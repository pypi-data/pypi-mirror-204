from typing import Protocol, Optional, TYPE_CHECKING

from aioredis import Redis

from kmx.models import MessageEnvelope, RpcQuery, RpcResult

from kmx.services.logger import Logger
from kmx.services.locker import Locker


if TYPE_CHECKING:
    from kmx.agents import Agent


class Container(Protocol):
    """ """

    logger: Logger
    locker: Locker
    redis: Optional[Redis]

    def add_agent(self, agent: 'Agent'):
        """ """

    async def start(self):
        """ """

    async def send_message(self, message_envelope: MessageEnvelope):
        """ """

    async def rpc_call(self, rpc_envelope: RpcQuery) -> RpcResult:
        """ """
