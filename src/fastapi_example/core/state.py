import logging
from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager, AsyncExitStack, asynccontextmanager
from typing import TypedDict

import httpx
from fastapi import FastAPI
from starlette.datastructures import State

from fastapi_example.instrumentation import setup_logging
from fastapi_example.settings import Settings

logger = logging.getLogger(__name__)


class LifespanState(TypedDict):
    http_client: httpx.AsyncClient


class StatefulLifespan:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def __call__(self, app: FastAPI) -> AbstractAsyncContextManager[LifespanState]:
        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncIterator[LifespanState]:
            setup_logging(self._settings)

            async with AsyncExitStack() as stack:
                logger.info("Starting lifespan")
                http_client = await stack.enter_async_context(httpx.AsyncClient())

                yield {"http_client": http_client}

                logger.info("Exiting lifespan")

        return lifespan(app)


class RequestState(State):
    _state: LifespanState  # type: ignore[assignment]

    @property
    def http_client(self) -> httpx.AsyncClient:
        return self._state["http_client"]
