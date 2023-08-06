from typing import AsyncIterator, Callable, Coroutine, Any
import inspect

import asyncio

from kmx.models import MessageEnvelope


class DummyMessageConsumer:
    """ """

    def __init__(self,
                 request_messages_cb: Callable[[], list[MessageEnvelope]] | Coroutine[Any, Any, list[MessageEnvelope]] = None,
                 tick_delay: float = 0.5):
        """ """
        self._request_messages_cb = request_messages_cb
        self._tick_delay = tick_delay

    async def start(self):
        """ """

    async def stop(self):
        """ """

    async def consume_messages(self) -> AsyncIterator[MessageEnvelope]:
        """ """
        while True:
            await asyncio.sleep(self._tick_delay)
            messages = await self._request_new_messages()
            for message in messages:
                yield message

    async def _request_new_messages(self) -> list[MessageEnvelope]:
        """ """
        if self._request_messages_cb is None:
            return []

        if inspect.iscoroutinefunction(self._request_messages_cb):
            return await self._request_messages_cb()  # noqa

        return self._request_messages_cb()
