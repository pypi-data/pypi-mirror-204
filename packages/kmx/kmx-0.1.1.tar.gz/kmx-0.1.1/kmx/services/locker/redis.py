import asyncio
import time
from contextlib import asynccontextmanager

import aioredis
from aioredis.exceptions import RedisError

from kmx.services.logger import Logger
from kmx.services.logger.dummy import DummyLogger

from kmx.exceptions import LockTimeout


class RedisLocker:
    """ """
    def __init__(self,
                 redis_url: str,
                 logger: Logger | None = None,
                 tick: float = 0.5,
                 default_expires_in: int = 60,
                 prefix: str | None = None):
        """ """
        self._redis = aioredis.from_url(redis_url)
        self._logger = logger or DummyLogger()
        self._tick = tick
        self._default_expires_in = default_expires_in
        self._prefix = prefix or 'lock'

    @asynccontextmanager
    async def lock(self, identifier: str, expires_in: int | None = None, wait_time: int | None = None):
        """ """
        expires_in = expires_in if expires_in is not None else self._default_expires_in
        lock_info = time.time()
        async with self._wait(identifier, wait_time):
            try:
                await self._redis.setex(self._lock_id(identifier), expires_in, lock_info)
                yield
            finally:
                try:
                    await self._redis.delete(self._lock_id(identifier))
                except RedisError:
                    # ну и ладно
                    ...

    @asynccontextmanager
    async def wait(self, identifier: str, wait_time: int | None = None):
        """ """
        async with self._wait(identifier, wait_time):
            yield

    @asynccontextmanager
    async def _wait(self, identifier: str, wait_time: int | None = None):
        """ """
        started_at = time.monotonic()
        while True:
            if not await self._redis.exists(self._lock_id(identifier)):
                break
            await asyncio.sleep(self._tick)
            if not wait_time or (time.monotonic() - started_at) > wait_time:
                raise LockTimeout(f'Lock timeout for identifier {identifier}')
        yield

    def _lock_id(self, identifier: str) -> str:
        return f'{self._prefix}_{identifier}'
