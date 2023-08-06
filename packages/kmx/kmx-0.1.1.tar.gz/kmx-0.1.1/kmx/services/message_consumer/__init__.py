from typing import Protocol
from collections.abc import AsyncIterator

from kmx.models import MessageEnvelope


class MessageConsumer(Protocol):
    """ """

    async def start(self, topics: list[str] | set[str] | tuple[str]):
        ...

    async def stop(self):
        ...

    async def consume_messages(self) -> AsyncIterator[MessageEnvelope]:
        """ """
        ...
