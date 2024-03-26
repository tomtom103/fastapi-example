import logging
from typing import Any

import ujson
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
)
from fastapi.responses import (
    JSONResponse as _JSONResponse,
)

logger = logging.getLogger(__name__)


class JSONResponse(_JSONResponse):
    """
    JSON response using the high-performance ujson library to serialize data to JSON.
    """

    def render(self, content: Any) -> bytes:
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


__all__ = [
    "FileResponse",
    "HTMLResponse",
    "JSONResponse",
    "PlainTextResponse",
    "RedirectResponse",
    "Response",
    "StreamingResponse",
]
