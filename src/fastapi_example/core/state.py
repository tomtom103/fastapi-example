from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from typing import TypedDict

import httpx
from fastapi import FastAPI
from starlette.datastructures import State

from fastapi_example.redis import AsyncClient as AsyncRedisClient
from fastapi_example.settings import Settings


class LifespanState(TypedDict):
    http_client: httpx.AsyncClient
    redis_client: AsyncRedisClient


class StatefulLifespan:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncIterator[LifespanState]:
        async with AsyncExitStack() as stack:
            http_client = await stack.enter_async_context(httpx.AsyncClient())
            redis_client = await stack.enter_async_context(AsyncRedisClient())

            yield {"http_client": http_client, "redis_client": redis_client}


class RequestState(State):
    _state: LifespanState  # type: ignore[assignment]

    @property
    def http_client(self) -> httpx.AsyncClient:
        return self._state["http_client"]

    @property
    def redis_client(self) -> AsyncRedisClient:
        return self._state["redis_client"]
