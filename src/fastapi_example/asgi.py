from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager

import httpx
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from .settings import Settings, get_settings
from .state import RequestState


def create_app(*, settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[RequestState]:
        # Setup
        async with AsyncExitStack() as stack:
            http_client = await stack.enter_async_context(httpx.AsyncClient())

            yield {"http_client": http_client}

    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.API_NAME,
        lifespan=lifespan,
    )

    @app.get("/", include_in_schema=False)
    def redirect_docs() -> RedirectResponse:
        return RedirectResponse("/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    return app
