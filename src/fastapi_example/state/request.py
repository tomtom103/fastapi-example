from typing import TYPE_CHECKING

from fastapi.requests import Request

if TYPE_CHECKING:
    from .state import RequestState

    class StatefulRequest(Request):
        state: RequestState  # type: ignore[assignment]

else:
    StatefulRequest = Request
