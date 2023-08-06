from typing import Protocol, Optional, Any, TYPE_CHECKING

from kmx.models import Message, MessageEnvelope
from kmx.containers import Container
from kmx.services.locker import Locker
from kmx.services.logger import Logger


if TYPE_CHECKING:
    from kmx.behaviours import Behaviour


class Agent(Protocol):
    """ """

    name: str
    topics: list[str]
    container: Container
    behaviours: list['Behaviour']
    logger: Logger

    def add_behaviour(self, benaviour: 'Behaviour'):
        """ """
        ...

    # ------------------------------------------------------------------------------------------------------------------
    # Инициализация
    # ------------------------------------------------------------------------------------------------------------------
    async def start(self):
        """ """

    # ------------------------------------------------------------------------------------------------------------------
    # Работа с сообщениями
    # ------------------------------------------------------------------------------------------------------------------
    async def send_message(self, to: str, message: Message, reply_to: Optional[Message] = None):
        """ """

    async def receive_message(self, message_envelope: MessageEnvelope):
        """ """

    async def rpc_call(self, to: str, what: str, params: Any, response_class: Optional[Any]) -> Any:
        """ """

    def locker(self) -> Locker:
        """ """
