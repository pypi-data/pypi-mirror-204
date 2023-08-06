from typing import Protocol

from kmx.models import MessageEnvelope


class MessageProducer(Protocol):
    """ """

    async def start(self):
        """ """

    async def stop(self):
        """ """

    async def send_message(self, message: MessageEnvelope):
        """ """
