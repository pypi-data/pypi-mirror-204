from typing import Protocol


class DbInitializer(Protocol):
    """ """
    async def init_db(self):
        """ """