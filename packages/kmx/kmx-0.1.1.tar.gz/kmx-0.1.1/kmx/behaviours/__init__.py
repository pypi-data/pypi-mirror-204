from typing import Protocol, Callable, Optional

from kmx.models import MessageEnvelope
from kmx.agents import Agent
from kmx.services.locker import Locker
from kmx.services.logger import Logger


class Behaviour(Protocol):
    """ """
    agent: Agent
    logger: Logger

    async def run(self):
        """ """

    async def match_message(self, message_envelope: MessageEnvelope) -> Optional[Callable]:
        """ """

    def locker(self) -> Locker:
        """ """
