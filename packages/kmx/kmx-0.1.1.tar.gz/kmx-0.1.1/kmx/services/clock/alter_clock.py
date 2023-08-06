from typing import Optional

import datetime
from collections import namedtuple


TimeSavePoint = namedtuple('TimeSavePoint', 'external_now local_now')


class TestClock:

    def __init__(self):
        self.savepoint: Optional[TimeSavePoint] = None

    def reset(self):
        self.savepoint = None

    def set_time(self, now: datetime.datetime):
        """ """
        if now.tzinfo is None:
            # Если
            now = now.replace(tzinfo=datetime.timezone.utc)

        self.savepoint = TimeSavePoint(external_now=now, local_now=datetime.datetime.now(datetime.timezone.utc))

    def now(self) -> datetime.datetime:
        """ """
        if self.savepoint is None:
            return self._local_now()

        return self._local_now() + datetime.timedelta(
            seconds=(self.savepoint.external_now - self.savepoint.local_now).total_seconds())

    @staticmethod
    def _local_now() -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)
