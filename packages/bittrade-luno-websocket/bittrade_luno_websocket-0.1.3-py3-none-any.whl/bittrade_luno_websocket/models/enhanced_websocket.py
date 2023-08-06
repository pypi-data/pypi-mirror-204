from logging import getLogger
from typing import Any, cast
from reactivex.subject import BehaviorSubject
from elm_framework_helpers.websockets.models import EnhancedWebsocket as OriginalEnhancedWebsocket

import orjson
import websocket

logger = getLogger(__name__)
raw_logger = getLogger("bittrade_luno_websocket.raw_socket.sent")


class EnhancedWebsocket(OriginalEnhancedWebsocket):
    def send_message(self, message: Any) -> int | str:
        return self.send_json(message)

    def prepare_request(self, message: Any) -> tuple[str, bytes]:
        self._id += 1
        return f"id{self._id}", orjson.dumps(message)



__all__ = [
    "EnhancedWebsocket",
]
