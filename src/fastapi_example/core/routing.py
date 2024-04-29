import logging
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import APIRouter as _APIRouter
from fastapi import Request as _Request
from fastapi import Response as _Response
from fastapi.responses import UJSONResponse
from fastapi.routing import APIRoute as _APIRoute

from .models import Request

logger = logging.getLogger(__name__)


class APIRoute(_APIRoute):
    def get_route_handler(self) -> Callable[[_Request], Coroutine[Any, Any, _Response]]:
        original_handler = super().get_route_handler()

        async def custom_route_handler(request: _Request) -> _Response:
            _request = Request(request.scope, request.receive)
            logger.warning("Request URL: %s", str(_request.url))
            return await original_handler(_request)

        return custom_route_handler


class APIRouter(_APIRouter):
    def __init__(
        self,
        route_class: type[APIRoute] = APIRoute,
        default_response_class: type[_Response] = UJSONResponse,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            route_class=route_class,
            default_response_class=default_response_class,
            **kwargs,
        )
