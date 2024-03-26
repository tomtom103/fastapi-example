import logging

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from .core import StatefulLifespan
from .routes import get_router
from .settings import Settings, get_settings

logger = logging.getLogger(__name__)


def create_app(*, settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    stateful_lifespan = StatefulLifespan(settings)

    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.API_NAME,
        lifespan=stateful_lifespan.lifespan,
    )

    app.include_router(get_router(settings))

    @app.get("/", include_in_schema=False)
    def redirect_docs() -> RedirectResponse:
        return RedirectResponse("/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    return app
