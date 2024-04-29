from functools import partial

import uvicorn

from .instrumentation.logging import get_logging_config
from .main import get_app
from .settings import get_settings


def main() -> None:
    settings = get_settings()

    logging_config = get_logging_config(settings)

    app_factory = partial(get_app, settings=settings, log_config=logging_config)

    uvicorn.run(
        app_factory,
        host=settings.API_HOST,
        port=settings.API_PORT,
        factory=True,
        log_config=logging_config,
    )


def cli() -> None:
    import typer

    typer.run(main)
