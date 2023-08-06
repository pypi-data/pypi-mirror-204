from typing import Optional

import abc
from collections import deque

from aioredis import Redis

from kmx.models import MessageEnvelope
from kmx.containers import Container
from kmx.agents import Agent

from kmx.services.logger import Logger
from kmx.services.locker import Locker


class ContainerContext:
    """ """
    containers = deque()

    @classmethod
    def push_container(cls, container: Container):
        """ """
        ContainerContext.containers.append(container)

    @classmethod
    def pop_container(cls) -> Optional[Container]:
        """ """
        return ContainerContext.containers.pop() if ContainerContext.containers else None

    @classmethod
    def current_container(cls) -> Optional[Container]:
        """ """
        return ContainerContext.containers[-1] if ContainerContext.containers else None


class ContainerBase(metaclass=abc.ABCMeta):
    """ """
    def __init__(self, locker: Locker, logger: Logger, redis: Optional[Redis] = None):
        """ """
        self.agents: list[Agent] = []
        self.agents_map: dict[str, Agent] = {}
        self.locker = locker
        self.logger = logger
        self.redis = redis

    def __enter__(self) -> Container:
        """ """
        ContainerContext.push_container(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ """
        ContainerContext.pop_container()

    def add_agent(self, agent: Agent):
        """ """
        if not agent.name:
            raise Exception(f'Не указано имя агента при добавлении в контейнер: {type(agent)}')
        if agent.name in self.agents_map:
            raise Exception(f'Agent with name `{agent.name}` already exists in the container')
        self.agents_map[agent.name] = agent

        self.agents.append(agent)

        self.logger.info(f'Agent `{agent.name}` added to container')

    @abc.abstractmethod
    async def start(self):
        """ """
        ...

    @abc.abstractmethod
    async def send_message(self, message_envelope: MessageEnvelope):
        """ """
        ...

    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        """ """
        return self.agents_map.get(name)
