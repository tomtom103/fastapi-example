from typing import Any

from redis.asyncio import ConnectionPool as AsyncConnectionPool
from redis.asyncio import Redis as AsyncRedis

from fastapi_example._compat import Self
from fastapi_example.settings import RedisSettings, get_redis_settings


class AsyncClient:
    def __init__(self, *, settings: RedisSettings | None = None) -> None:
        self._settings = settings or get_redis_settings()
        self.pool: AsyncConnectionPool | None = None
        self.connection: AsyncRedis | None = None

    async def __aenter__(self) -> Self:
        self.pool = AsyncConnectionPool.from_url(
            f"redis://{self._settings.REDIS_HOST}:{self._settings.REDIS_PORT}"
        )
        self.connection = AsyncRedis(connection_pool=self.pool)

        return self

    async def __aexit__(self, *_: Any, **__: Any) -> None:
        if self.pool is not None:
            await self.pool.aclose()
        if self.connection is not None:
            await self.connection.aclose(
                close_connection_pool=False,  # We close it ourselves
            )
