from functools import partial

import uvicorn

from .asgi import create_app
from .settings import get_settings


def main() -> None:
    settings = get_settings()

    app_factory = partial(create_app, settings=settings)

    uvicorn.run(
        app_factory, host=settings.API_HOST, port=settings.API_PORT, factory=True
    )


def cli() -> None:
    import typer

    typer.run(main)
