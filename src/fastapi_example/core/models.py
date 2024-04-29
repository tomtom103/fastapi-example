from typing import cast

from fastapi import Request as _Request

try:
    import ujson
except ImportError:
    import json as ujson  # type: ignore[no-redef]

import logging
from typing import Any

import ujson
from fastapi.responses import (
    JSONResponse as _JSONResponse,
)

from .state import RequestState

logger = logging.getLogger(__name__)


class Request(_Request):
    async def body(self) -> bytes:
        """
        Read the body like normal but store it in the request scope for use in middlewares
        """
        if not hasattr(self, "_body"):
            chunks = []
            async for chunk in self.stream():
                chunks.append(chunk)
            self.scope["_body"] = self._body = b"".join(chunks)
        return self._body

    async def json(self) -> str:
        """
        Like the super json method, but will raise an error if null bytes are found in the JSON, also use
        ujson to parse the JSON when available.
        """
        if not hasattr(self, "_json"):
            body = await self.body()
            if b"\\u0000" in body:
                raise ValueError("Invalid JSON body containing null bytes")
            self._json = ujson.loads(body)
        return cast(str, self._json)

    @property
    def state(self) -> RequestState:
        if not hasattr(self, "_state"):
            # Ensure 'state' has an empty dict if it's not already populated.
            self.scope.setdefault("state", {})
            # Create a state instance with a reference to the dict in which it should
            # store info
            self._state = RequestState(self.scope["state"])
        return cast(RequestState, self._state)


class JSONResponse(_JSONResponse):
    """
    JSON response using the high-performance ujson library to serialize data to JSON.
    """

    def render(self, content: Any) -> bytes:
        return ujson.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
