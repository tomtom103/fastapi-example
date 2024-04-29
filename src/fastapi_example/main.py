import logging.config
from typing import Any

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from .core import StatefulLifespan
from .instrumentation import get_logging_config
from .routes import get_router
from .settings import Settings, get_settings


def get_app(
    *, settings: Settings | None = None, log_config: dict[str, Any] | None = None
) -> FastAPI:
    settings = settings or get_settings()

    if log_config is None:
        log_config = get_logging_config(settings)
        logging.config.dictConfig(log_config)

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
