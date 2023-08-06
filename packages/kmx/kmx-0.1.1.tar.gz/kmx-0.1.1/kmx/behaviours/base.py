from typing import Callable, Optional
import abc

from kmx.models import MessageEnvelope
from kmx.agents import Agent
from kmx.services.locker import Locker
from kmx.services.logger import Logger
from kmx.services.logger.dummy import DummyLogger

from kmx.agents.base import AgentContext


class BehaviourBase(metaclass=abc.ABCMeta):
    """ """

    def __init__(self, logger: Logger, agent: Optional[Agent] = None):
        self.agent = agent or AgentContext.current_agent()
        self.logger = logger

        self.agent.add_behaviour(self)

    def locker(self) -> Locker:
        """ """
        return self.agent.locker()

    async def run(self):
        """ """

    async def internal_run(self):
        await self.run()

    async def match_message(self, message_envelope: MessageEnvelope) -> Optional[Callable]:
        return None
