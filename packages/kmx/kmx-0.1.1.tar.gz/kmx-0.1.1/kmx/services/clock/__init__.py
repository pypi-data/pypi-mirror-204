from typing import Protocol

import datetime


class Clock(Protocol):
    """ Сервис, с помощью которого мы получаем текущее время """
    def set_time(self, now: datetime.datetime):
        """Устанавливает текущее время"""
    def now(self) -> datetime.datetime:
        """Возвращает текущее время"""

    def reset(self):
        """Возврат часов к нормальному потоку"""