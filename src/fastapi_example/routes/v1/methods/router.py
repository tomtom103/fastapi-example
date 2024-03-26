from fastapi_example.core import APIRouter, JSONResponse, Request
from fastapi_example.settings import Settings


def get_router(settings: Settings) -> APIRouter:
    router = APIRouter()

    @router.get("/get")
    async def get(*, request: Request) -> JSONResponse:
        http_client = request.state.http_client
        response = await http_client.get("https://httpbin.org/get")
        response.raise_for_status()
        return JSONResponse({"response": response.json()})

    return router
