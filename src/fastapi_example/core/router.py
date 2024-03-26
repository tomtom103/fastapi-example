import logging
from typing import Any

from fastapi import APIRouter as _APIRouter
from fastapi import Response as _Response
from fastapi.responses import UJSONResponse

from .routing import APIRoute

logger = logging.getLogger(__name__)


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
