from typing import Optional, Any, Awaitable, Callable

import asyncio
import json
import inspect

from aioredis import Redis
from pydantic import BaseModel, ValidationError

from kmx.models import Message, MessageEnvelope, RpcQuery, RpcResult
from kmx.agents import Agent
from kmx.services.message_consumer import MessageConsumer
from kmx.services.message_producer import MessageProducer
from kmx.services.locker import Locker

from kmx.services.logger import Logger
from kmx.services.logger.dummy import DummyLogger

from kmx.db import DbInitializer

from .base import ContainerBase
from ..exceptions import RpcTimeout, RpcIncompatibleParams, RpcBadQuery


class KmxContainer(ContainerBase):
    """ """
    def __init__(self,
                 message_consumer: MessageConsumer,
                 message_producer: MessageProducer,
                 locker: Locker,
                 logger: Logger,
                 redis: Optional[Redis] = None,
                 db_initializer: Optional[DbInitializer] = None):
        """ """
        super().__init__(logger=logger, locker=locker, redis=redis)

        self.message_consumer = message_consumer
        self.message_producer = message_producer
        self.db_initializer = db_initializer

        self.rpc_map: dict[tuple[str, str], Callable] = {}

    async def start(self):
        """ """
        self.logger.info('Starting container')

        if not self.agents:
            self.logger.error('Container has no agents. Finishing')
            return

        # init db
        if self.db_initializer is not None:
            await self.db_initializer.init_db()
            self.logger.info('Database initialized')

        # start producer
        await self.message_producer.start()

        # create task list
        tasks = [
            asyncio.create_task(self.consume_messages())
        ]
        if self.redis is not None:
            self._parse_agents_rpc()
            tasks.append(self.listen_rpc_queue())

        for agent in self.agents:
            await agent.start()
            for behav in agent.behaviours:
                tasks.append(asyncio.create_task(behav.run()))

        await asyncio.gather(*tasks)

    async def send_message(self, message_envelope: MessageEnvelope):
        """ """
        await self.message_producer.send_message(message_envelope)

    # ------------------------------------------------------------------------------------------------------------------
    # Обработка входящих сообщений
    # ------------------------------------------------------------------------------------------------------------------
    async def consume_messages(self):
        topics = []
        for agent in self.agents:
            topics.extend(agent.topics)
        try:
            await self.message_consumer.start(topics=set(topics))
        except:
            self.logger.exception('Cannot start message consumer')

        try:
            async for message in self.message_consumer.consume_messages():
                self.logger.debug(f'Получено сообщение {message.json(ensure_ascii=False)}')
                agent = self.get_agent_by_name(message.receiver)
                if agent is not None:
                    await agent.receive_message(message)
        finally:
            await self.message_consumer.stop()

    # ------------------------------------------------------------------------------------------------------------------
    # Обработка RPC сообщений
    # ------------------------------------------------------------------------------------------------------------------
    async def listen_rpc_queue(self):
        """ """
        queue_names = [self._rpc_queue_name(agent.name) for agent in self.agents]

        self.logger.info(f'Start listening rpc queues `{queue_names}`')

        async with self.redis:

            while True:
                try:
                    queue_name, message = await self.redis.blpop(queue_names)
                    self.logger.debug(f'Got rpc call from queue {queue_name}: {message}')

                    #await self._handle_rpc_call(message)
                    asyncio.create_task(self._handle_rpc_call(message))

                except RpcBadQuery as e:
                    self.logger.error(f'Got rpc call with bad query: {e}')
                except Exception as e:
                    self.logger.exception('Error on handle rpc call')
                    await asyncio.sleep(0.05)

    async def _handle_rpc_call(self, message: bytes):
        """ """
        try:
            rpc_query: RpcQuery = RpcQuery.parse_raw(message)
        except ValidationError as e:
            rpc_call_uid = self._try_get_rpc_call_uid(message)
            if rpc_call_uid is None:
                # отправляем ответ с ошибкой
                raise RpcBadQuery(f'Cannot read rpc_call_uid from message {message}')
            else:
                error_msg = f'Rpc bad query: {e}'
                self.logger.error(f'Got rpc with bad query: {e}')
                await self._reply_rpc_error(rpc_call_uid, error_msg, timeout=5)
                return

        # Check rpc timeout
        if (await self.redis.delete(self._rpc_expire_key(rpc_query.rpc_call_uid))) == 0:
            # timeout - do nothing
            self.logger.warning(f'Got rpc call with timeout: {rpc_query}')
            return

        # get rpc_worker
        rpc_executor: Callable = self.rpc_map.get((rpc_query.rpc_to, rpc_query.rpc_name))
        if rpc_executor is None:
            error_msg = f'Rpc executor for {rpc_query.rpc_to}.{rpc_query.rpc_name} not found'
            self.logger.error(error_msg)

            await self._reply_rpc_error(rpc_query.rpc_call_uid, error_msg, rpc_query.timeout)
            return

        # execute rpc
        try:
            params_found, params = self._rpc_params_for_executor(rpc_executor, rpc_query.data)
        except ValidationError as e:
            error_msg = \
                f'Got incompatible params for rpc executor {rpc_query.rpc_to}.{rpc_query.rpc_name}: {e}'
            self.logger.error(error_msg)

            await self._reply_rpc_error(rpc_query.rpc_call_uid, error_msg, rpc_query.timeout)
            return

        try:
            if params_found:
                executor_result = await rpc_executor(params=params)
            else:
                executor_result = await rpc_executor(params)
        except Exception as e:
            error_msg = \
                f'Rpc remote error: {e}'
            self.logger.exception(f'Error on rpc {rpc_query.rpc_to}.{rpc_query.rpc_name} execution')
            await self._reply_rpc_error(rpc_query.rpc_call_uid, error_msg, rpc_query.timeout)
            return

        # всё ок, отправляем результат
        await self._reply_rpc_result(rpc_query, executor_result)

    async def _reply_rpc_result(self, rpc_query: RpcQuery, executor_result: Any):
        """ """
        result_key = self._rpc_results_key(rpc_call_uid=rpc_query.rpc_call_uid)

        if isinstance(executor_result, BaseModel):
            data = executor_result.dict()
        elif isinstance(executor_result, dict):
            data = executor_result
        else:
            # непонятное значение, попробуем передать как есть
            data = {'__rpc_raw_result__': executor_result}

        executor_result = RpcResult(rpc_call_uid=rpc_query.rpc_call_uid, data=data)

        # send result
        await self.redis.lpush(result_key, executor_result.json(ensure_ascii=False).encode())
        # set timeout for result
        await self.redis.expire(result_key, rpc_query.timeout)

        return

    async def _reply_rpc_error(self, rpc_call_uid: str, error: str, timeout: int):
        """ """
        result_key = self._rpc_results_key(rpc_call_uid)
        result = RpcResult(rpc_call_uid=rpc_call_uid, error=error)

        # send result
        await self.redis.lpush(result_key, result.json(ensure_ascii=False).encode())
        # set timeout for result
        await self.redis.expire(result_key, timeout)

        return

    @staticmethod
    def _try_get_rpc_call_uid(self, rpc_message: bytes) -> Optional[str]:
        """ """
        result = None

        try:
            data = json.loads(rpc_message)
            if isinstance(data, dict):
                result = data.get('rpc_call_uid')
        except:
            ...

        return result

    async def rpc_call(self, rpc_query: RpcQuery) -> RpcResult:
        """ """
        # set timeout for receiver
        await self.redis.setex(
            self._rpc_expire_key(rpc_query.rpc_call_uid),
            rpc_query.timeout,
            1  # any value
        )
        # send request
        await self.redis.rpush(
            self._rpc_queue_name(rpc_query.rpc_to),
            rpc_query.json(ensure_ascii=False).encode()
        )

        # wait for results (with timeout)
        async with self.redis:
            result_message = await self.redis.blpop(
                self._rpc_results_key(rpc_query.rpc_call_uid),
                rpc_query.timeout
            )

        if result_message is None:
            raise RpcTimeout(
                f'Timeout for rpc call `{rpc_query.rpc_to}.{rpc_query.rpc_name}` ({rpc_query.timeout} sec.)')

        _, message = result_message

        return RpcResult.parse_raw(message)

    @staticmethod
    def _rpc_queue_name(to: str) -> str:
        return f'kmx:{to}:rpc_queue'

    @staticmethod
    def _rpc_expire_key(rpc_call_uid: str) -> str:
        return f'kmx:rpc_expiry_key:{rpc_call_uid}'

    @staticmethod
    def _rpc_results_key(rpc_call_uid: str) -> str:
        """ """
        return f'kmx:rpc_result:{rpc_call_uid}'

    def _parse_agents_rpc(self):
        """ """
        self.rpc_map = {}
        for agent in self.agents:
            for _, func in inspect.getmembers(agent, predicate=inspect.iscoroutinefunction):
                if hasattr(func, '__kmx_rpc_function__'):
                    self.rpc_map[(agent.name, func.__kmx_rpc_function__)] = func
        return

    @staticmethod
    def _rpc_params_for_executor(executor: Any, params_dict: dict) -> tuple[bool, Any]:
        """ """
        params = params_dict

        arg_params = inspect.signature(executor).parameters.get('params')

        if arg_params is None:
            return False, params

        if issubclass(arg_params.annotation, BaseModel):
            params = arg_params.annotation.parse_obj(params)

        return True, params


# Compability
GenericContainer = KmxContainer
