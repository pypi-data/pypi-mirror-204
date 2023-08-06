from typing import AsyncIterable, Any, Optional

import asyncio
import datetime
import uuid

from pydantic import BaseModel, ValidationError

from beanie.operators import And, In, Eq, Or, GTE, Set
import pymongo

from kmx.services.locker import Locker
from kmx.exceptions import LockTimeout

from kmx.services.logger import Logger
from kmx.services.logger.dummy import DummyLogger

from kmx.services.clock import Clock
from kmx.services.clock.system_clock import SystemClock

from .flow import Flow, FlowPack
from .models import FlowRun
from .tasks import FlowTask
from .db import DbFlowRun, DbFlowRunState, DbFlowTaskRun, DbFlowTaskRunState, DbActiveFlowRunView, \
    DbFinishedFlowTaskRunView
from .exceptions import DelayFlowTask, StopFlowRun


class FlowProcessor:

    def __init__(self, flows: FlowPack, locker: Locker, logger: Optional[Logger] = None, clock: Optional[Clock] = None):
        self.flows = flows
        self.locker = locker
        self.start_delay = 1
        self.delay = 0.05
        self.logger = logger or DummyLogger()
        self.clock = clock or SystemClock()

    async def run_flow(self, flow: Flow, params: Any = None, delay: int = None) -> DbFlowRun:
        """
        Run flow

        Args:
            flow: flow definition to run
            params: start params (dict or instance of BaseModel subclass)
            delay:
        """
        if not self.flows.flow_exists(flow):
            raise Exception(f'Flow `{flow.name}` not found')
        
        flow_run = DbFlowRun(
            flow_name=flow.name,
            uid=str(uuid.uuid4()).replace('-', ''),
            context={
                'flow_params': params.dict() if isinstance(params, BaseModel) else params
            },
            state=DbFlowRunState.ACTIVE,
            created_at=self.clock.now(),
            delayed_until=self.clock.now() + datetime.timedelta(seconds=delay) if delay else None,
            finished_at=None
        )

        await flow_run.create()

        self.logger.info(f'Flow `{flow.name}` started with params {params} and delay {delay} sec')

        return flow_run

    async def scheduler(self, once: bool = False):
        """ """
        self.logger.info('Start flow scheduling')
        await asyncio.sleep(self.start_delay)
        while True:
            has_active_runs = False
            async for flow_run in self.fetch_active_flow_runs():
                has_active_runs = True
                if flow_run.delayed_until is not None and \
                        flow_run.delayed_until > self.clock.now():
                    continue
                try:
                    async with self.locker.lock(flow_run.uid):
                        await self.handle_active_flow_run(flow_run)
                except LockTimeout:
                    # поток уже заблокирован, выполняется где-то
                    continue
                except Exception as e:
                    raise
            if once and not has_active_runs:
                break
            await asyncio.sleep(self.delay)

    def fetch_active_flow_runs(self) -> AsyncIterable[DbActiveFlowRunView]:
        """ """
        filter_expr = And(
            In(DbFlowRun.flow_name, self.flows.flow_names),
            Eq(DbFlowRun.state, DbFlowRunState.ACTIVE),
            # Or(
            #     Eq(DbFlowRun.delayed_until, None),
            #     GTE(DbFlowRun.delayed_until, datetime.datetime.now(datetime.timezone.utc))
            # )
        )

        return DbFlowRun.find(filter_expr).sort([('created_at', pymongo.ASCENDING)]).project(DbActiveFlowRunView)

    async def handle_active_flow_run(self, flow_run_view: DbActiveFlowRunView):
        """ """
        # Получаем список уже выполненных задач
        done_task_names = []

        flow_run = await DbFlowRun.find_one(DbFlowRun.id == flow_run_view.id)
        if flow_run is None:
            # Flow run does not exist, skipping
            return

        async for task_run in DbFlowTaskRun\
                .find(DbFlowTaskRun.flow_run_uid == flow_run_view.uid).project(DbFinishedFlowTaskRunView):
            if task_run.state == DbFlowTaskRunState.ACTIVE:
                # There is an active task for the flow. Skip!
                return
            done_task_names.append(task_run.task_name)

        flow = self.flows.get_flow_by_name(flow_run_view.flow_name)
        tasks_to_run = self.get_tasks_to_run(flow, done_task_names)

        if not tasks_to_run:
            # There is no a task in the flow to run. Finalize it!
            await flow_run.update(Set({
                DbFlowRun.state: DbFlowRunState.FINISHED,
                DbFlowRun.finished_at: self.clock.now()
            }))
            self.logger.info(
                f'Flow `{flow.name}` with params {flow_run.context.get("flow_params")} finished: all tasks completed')
        else:
            for flow_task in tasks_to_run:
                asyncio.create_task(self.run_task(flow, flow_run, flow_task))

    def get_tasks_to_run(self, flow: Flow, done_task_names: list[str]) -> list[FlowTask]:
        """ """
        if not done_task_names:
            return flow.heads()

        tasks = []
        for done_task_name in done_task_names:
            tasks.extend([t for t in flow.successors(done_task_name) if t.name not in done_task_names])

        return tasks

    async def run_task(self, flow: Flow, flow_run: DbFlowRun, flow_task: FlowTask):
        """ """
        # create task_run for flow_task
        task_run = DbFlowTaskRun(
            flow_run_uid=flow_run.uid,
            task_name=flow_task.name,
            state=DbFlowTaskRunState.ACTIVE,
            created_at=self.clock.now(),
            finished_at=None
        )
        await task_run.insert()

        try:
            context = flow.context_model.parse_obj(
                flow_run.context) if flow.context_model is not None else flow_run.context
        except ValidationError as e:
            # Cannot parse context to desired model correctly. Stopping this flow
            await task_run.delete()

            context = flow_run.context
            context['_error'] = {
                'code': 'validation-error',
                'text': f'{e}'
            }

            await flow_run.update(Set({
                DbFlowRun.state: DbFlowTaskRunState.FINISHED,
                DbFlowRun.finished_at: self.clock.now(),
                DbFlowRun.context: context
            }))
            self.logger.error(
                f'Flow `{flow.name}` with params {context.get("flow_params")} finished with '
                f'context validation error: {e}')
            return

        try:
            await flow_task.run(context, FlowRun(uid=flow_run.uid, flow_name=flow_run.flow_name))
        except StopFlowRun as e:
            context = context.dict() if isinstance(context, BaseModel) else context
            context['_reason'] = {
                'code': 'worflow-stopped',
                'text': f'Worflow was stopped: {e}'
            }
            await flow_run.update(Set({
                DbFlowRun.state: DbFlowTaskRunState.FINISHED,
                DbFlowRun.finished_at: self.clock.now(),
                DbFlowRun.context: context
            }))
            await task_run.delete()
            self.logger.info(
                f'Flow `{flow.name}` with params {context.get("flow_params")} finished by command: {e}'
            )

        except DelayFlowTask as e:
            await flow_run.update(Set({
                DbFlowRun.delayed_until: self.clock.now() + datetime.timedelta(seconds=e.delay),
                DbFlowRun.context: context.dict() if isinstance(context, BaseModel) else context
            }))
            await task_run.delete()

        except Exception as e:
            # получено непонятное сообщение, финализируем даг
            self.logger.exception(
                f'Исключение при попытке выполнения шага {task_run.task_name} потока {flow_run.flow_name}')
            context = context.dict() if isinstance(context, BaseModel) else context
            context['_reason'] = {
                'code': 'exception',
                'text': f'{e}'
            }
            await flow_run.update(Set({
                DbFlowRun.state: DbFlowTaskRunState.FINISHED,
                DbFlowRun.finished_at: self.clock.now(),
                DbFlowRun.context: context
            }))
            await task_run.delete()
            self.logger.error(
                f'Flow `{flow.name}` with params {context.get("flow_params")} finished with exception: {e}'
            )

        else:
            # update flow context after task run
            await flow_run.update(Set({
                DbFlowRun.context: context.dict() if isinstance(context, BaseModel) else context
            }))

            # in any case mark task_run as finished
            await task_run.update(Set({
                DbFlowTaskRun.state: DbFlowTaskRunState.FINISHED,
                DbFlowTaskRun.finished_at: self.clock.now()
            }))
