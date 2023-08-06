import datetime


class SystemClock:
    """ """
    def set_time(self, now: datetime.datetime):
        """Системные часы не позволяют устанавливать текущее время"""
        pass

    def reset(self):
        """Системные часы на позволяют резетить время к нормальному потоку"""

    def now(self) -> datetime.datetime:
        """ """
        return datetime.datetime.now(datetime.timezone.utc)
