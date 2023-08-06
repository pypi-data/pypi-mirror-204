from typing import Callable, Optional

from kmx.models import MessageEnvelope

from .base import BehaviourBase


class SimpleBehaviour(BehaviourBase):
    """ """

    async def run(self):
        """ """
        # по умолчанию ничего не делаем

    async def match_message(self, message_envelope: MessageEnvelope) -> Optional[Callable]:
        """ """
        return None
