from typing import Any, Optional

import abc
import asyncio

from beanie.operators import And, Eq

from kmx.flows import Flow, FlowPack, FlowProcessor
from kmx.flows.db import DbFlowRun, DbFlowTaskRun, DbFlowRunState, DbFlowTaskRunState

from kmx.services.logger import Logger

from .base import BehaviourBase


class FlowBehaviour(BehaviourBase):
    """ """
    DbFlowRun = DbFlowRun
    DbFlowRunState = DbFlowTaskRunState

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)
        self.flow_processor: Optional[FlowProcessor] = None
        self.flows: Optional[FlowPack] = None

    @abc.abstractmethod
    def create_flows(self) -> FlowPack:
        """ """

    def create_flow_processor(self) -> FlowProcessor:
        """ """
        return FlowProcessor(
            flows=self.flows,
            logger=self.logger,
            locker=self.locker()
        )

    async def run(self):
        """ 
        Старт поведения по работе с потоками
        """
        self.flows = self.create_flows()
        self.flow_processor = self.create_flow_processor()

        self.logger.info(f'Added flows: {",".join(self.flows.flow_names)}')

        asyncio.create_task(self.flow_processor.scheduler())

    async def run_flow(self, flow: Flow, params: Any = None, delay: int = None):
        """ """
        await self.flow_processor.run_flow(
            flow=flow,
            params=params,
            delay=delay
        )

    async def get_flow_run_by_uid(self, flow_name: str, flow_run_uid: str) -> Optional[DbFlowRun]:
        """ """
        search_criteria = And(
            Eq(DbFlowRun.flow_name, flow_name),
            Eq(DbFlowRun.uid, flow_run_uid)
        )

        return await DbFlowRun.find_one(search_criteria)
