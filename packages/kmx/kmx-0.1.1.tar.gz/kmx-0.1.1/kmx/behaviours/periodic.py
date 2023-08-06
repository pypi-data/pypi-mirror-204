from typing import Optional
import asyncio

from kmx.services.logger import Logger

from .base import BehaviourBase


class PeriodicBehaviour(BehaviourBase):
    """ """

    def __init__(self, logger: Logger, period: int, start_delay: int = -1):
        """ """
        super().__init__(logger=logger)
        self.period = period
        self.start_delay = start_delay if start_delay >= 0 else period

    async def internal_run(self):
        """ """
        # стартовая пауза
        await asyncio.sleep(self.start_delay)

        while True:
            try:
                await self.run()
            except Exception as e:
                self.logger.exception(f'Ошибка запуска периодического задания у {self}')
            # Пауза между тиками
            await asyncio.sleep(self.period)

    async def run(self):
        """ """
        ...