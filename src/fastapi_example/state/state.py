from typing import TypedDict

import httpx

# from starlette.datastructures import State


class RequestState(TypedDict):
    http_client: httpx.AsyncClient
