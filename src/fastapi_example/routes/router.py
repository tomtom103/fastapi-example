from fastapi_example.core import APIRouter
from fastapi_example.settings import Settings

from .methods import get_router as get_methods_router


def get_router(settings: Settings) -> APIRouter:
    router = APIRouter()

    router.include_router(get_methods_router(settings), tags=["Methods"])

    return router
