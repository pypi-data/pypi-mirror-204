import dataclasses
import time
from typing import Any, Literal

from bittrade_luno_websocket.models import endpoints


@dataclasses.dataclass(frozen=True)
class RequestMessage:
    method: Literal["GET", "POST"]
    endpoint: endpoints.Endpoints
    params: dict[str, Any] = dataclasses.field(default_factory=dict)
    url_format_arguments: dict[str, str] = dataclasses.field(default_factory=dict)
