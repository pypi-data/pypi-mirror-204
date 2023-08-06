import asyncio
import uuid
import inspect
from typing import Optional, Any, Callable

from pydantic import BaseModel

from kmx.models import Message, MessageEnvelope, RpcQuery
from kmx.containers import Container
from kmx.agents.base import AgentBase
from kmx.exceptions import RpcRemoteError
from kmx.services.locker import Locker

from kmx.services.logger import Logger


class KmxAgent(AgentBase):
    """ """

    def __init__(self, name: str, logger: Logger, topics: Optional[list[str]] = None,
                 container: Optional[Container] = None):
        super().__init__(name=name, logger=logger, topics=topics, container=container)
        self.message_handlers_map: dict[str, list[Callable]] = {}

    async def start(self):
        """ """
        self._parse_message_handlers()

    def locker(self) -> Locker:
        return self.container.locker

    # ------------------------------------------------------------------------------------------------------------------
    # Работа с сообщениями
    # ------------------------------------------------------------------------------------------------------------------
    async def send_message(self, to: str, message: Message, reply_to: Optional[Message] = None):
        """ """
        message_envelope = MessageEnvelope(
            sender=self.name,
            receiver=to,
            message=message,
            reply_to=reply_to
        )
        await self.container.send_message(message_envelope)

    async def rpc_call(self, to: str, what: str, params: Any, response_class: Optional[Any] = None) -> Any:
        """ """
        rpc_envelope = RpcQuery(
            rpc_call_uid=str(uuid.uuid4()).replace('-', ''),
            rpc_to=to,
            rpc_name=what,
            data=params.dict() if isinstance(params, BaseModel) else params
        )

        result = await self.container.rpc_call(rpc_envelope)

        if result.error is not None:
            raise RpcRemoteError(result.error)

        return response_class.parse_obj(result.data) if issubclass(response_class, BaseModel) else result.data

    async def receive_message(self, message_envelope: MessageEnvelope):
        """ """
        # составляем список обработчиков сообщения
        handlers = []
        if message_envelope.message.code in self.message_handlers_map:
            handlers.extend(self.message_handlers_map[message_envelope.message.code])

        for behav in self.behaviours:
            handler = await behav.match_message(message_envelope)

            if handler is not None:
                handlers.append(handler)

        if not handlers:
            self.logger.warning(f'Для сообщения с кодом {message_envelope.message.code} нет обработчика у агента '
                                f'{self.name}')

        for handler in handlers:
            asyncio.create_task(self._handle_message(handler, message_envelope))

    async def _handle_message(self, message_handler: Callable, message_envelope: MessageEnvelope):
        """ """
        try:
            kwargs = self._prepare_message_handler_params(message_handler, message_envelope)
            await message_handler(**kwargs)
        except Exception as e:
            self.logger.exception(f'Ошибка выполнения обработчика сообщения {message_envelope.message.data}')

    def _parse_message_handlers(self):
        """ """
        self.message_handlers_map = {}
        for behaviour in self.behaviours:
            for _, func in inspect.getmembers(behaviour, predicate=inspect.iscoroutinefunction):
                if hasattr(func, '__kmx_message_code__'):
                    self.message_handlers_map.setdefault(func.__kmx_message_code__, []).append(func)
        return

    @staticmethod
    def _prepare_message_handler_params(message_handler: Any, message_envelope: MessageEnvelope) -> dict:
        """ """
        handler_params = {}

        arg_message_envelope = inspect.signature(message_handler).parameters.get('message_envelope')
        arg_message_body = inspect.signature(message_handler).parameters.get('message_body')
        arg_reply_to_body = inspect.signature(message_handler).parameters.get('reply_to_body')

        if arg_message_envelope is not None:
            handler_params['message_envelope'] = message_envelope

        if arg_message_body is not None:
            if issubclass(arg_message_body.annotation, BaseModel):
                handler_params['message_body'] = arg_message_body.annotation.parse_obj(message_envelope.message.data)
            else:
                handler_params['message_body'] = arg_message_body

        if arg_reply_to_body is not None:
            if message_envelope.reply_to is None:
                handler_params['reply_to_body'] = None

            elif issubclass(arg_reply_to_body.annotation, BaseModel):
                handler_params['reply_to_body'] = arg_message_body.annotation.parse_obj(message_envelope.reply_to.data)

            else:
                handler_params['reply_to_body'] = arg_message_body

        return handler_params


GenericAgent = KmxAgent
