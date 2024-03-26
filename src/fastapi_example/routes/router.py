from fastapi_example.core import APIRouter
from fastapi_example.settings import Settings

from .v1 import get_router as get_v1_router


def get_router(settings: Settings) -> APIRouter:
    router = APIRouter()

    router.include_router(
        get_v1_router(settings),
        prefix="/v1",
    )

    return router
