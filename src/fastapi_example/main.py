from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.routing import Route

from .core import StatefulLifespan
from .routes import get_router
from .settings import Settings, get_settings


def get_app(
    *,
    settings: Settings | None = None,
) -> FastAPI:
    settings = settings or get_settings()

    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.API_NAME,
        lifespan=StatefulLifespan(settings),
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_headers="*",
                allow_methods="*",
                allow_origins="*",
            ),
            Middleware(
                GZipMiddleware,
                minimum_size=500,
                compresslevel=9,
            ),
        ],
    )

    app.include_router(get_router(settings))

    @app.get("/", include_in_schema=False)
    def redirect_docs() -> RedirectResponse:
        return RedirectResponse("/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    return app
