from fastapi import FastAPI
from prometheus_client import make_asgi_app


def instrument(app: FastAPI) -> None:
    app.mount("/metrics", make_asgi_app())


__all__ = ["instrument"]
