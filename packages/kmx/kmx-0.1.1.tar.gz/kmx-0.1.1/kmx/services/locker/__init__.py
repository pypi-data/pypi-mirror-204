from typing import Protocol

from contextlib import asynccontextmanager


class Locker(Protocol):
    """ """

    @asynccontextmanager
    async def lock(self, identifier: str, expires_in: int | None = None, wait_time: int | None = None):
        """ """
        yield
        

    @asynccontextmanager
    async def wait(self, identifier: str, wait_time: int | None = None):
        """ """
        yield
        
