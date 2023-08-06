from typing import Optional, Any

import abc
from collections import deque

from kmx.models import MessageEnvelope, Message
from kmx.agents import Agent
from kmx.containers import Container
from kmx.containers.base import ContainerContext
from kmx.behaviours import Behaviour
from kmx.services.logger import Logger


class AgentContext:
    """ """
    agents = deque()

    @classmethod
    def push_agent(cls, agent: Agent):
        """ """
        AgentContext.agents.append(agent)

    @classmethod
    def pop_agent(cls) -> Optional[Agent]:
        """ """
        return AgentContext.agents.pop() if AgentContext.agents else None

    @classmethod
    def current_agent(cls) -> Optional[Agent]:
        """ """
        return AgentContext.agents[-1] if AgentContext.agents else None


class AgentBase(metaclass=abc.ABCMeta):
    """ """

    def __init__(self, name: str, logger: Logger, topics: Optional[list[str]] = None,
                 container: Optional[Container] = None):
        """ """
        self.name = name
        self.topics = topics or [name]
        self.container = container or ContainerContext.current_container()
        self.behaviours: list[Behaviour] = []
        self.logger = logger

        self.container.add_agent(self)

    def __enter__(self) -> Agent:
        """ """
        AgentContext.push_agent(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ """
        AgentContext.pop_agent()

    def add_behaviour(self, behaviour: Behaviour):
        self.behaviours.append(behaviour)

        self.logger.info(f'Behaviour `{behaviour.__class__.__name__}` added to agent `{self.name}`')

    @abc.abstractmethod
    async def start(self):
        """ """

    @abc.abstractmethod
    async def send_message(self, to: str, message: Message, reply_to: Optional[Message] = None):
        """ """

    @abc.abstractmethod
    async def receive_message(self, message_envelope: MessageEnvelope):
        """ """

    @abc.abstractmethod
    async def rpc_call(self, to: str, what: str, params: Any, response_class: Optional[Any]) -> Any:
        """ """

