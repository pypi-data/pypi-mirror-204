import logging
from reactivex import observable, abc, disposable
from typing import Optional, Any
from websocket import WebSocketConnectionClosedException, WebSocketApp
from elm_framework_helpers.websockets.models import status, message_types, bundle
from elm_framework_helpers import schedulers
import orjson
from bittrade_luno_websocket.models import enhanced_websocket

logger = logging.getLogger(__name__)
raw_logger = logging.getLogger("bittrade_luno_websocket.raw_socket.received")

def raw_websocket_connection(
    url: str, scheduler: Optional[abc.SchedulerBase] = None
) -> observable.Observable[bundle.WebsocketBundle]:
    def subscribe(
        observer: abc.ObserverBase[bundle.WebsocketBundle],
        scheduler_: Optional[abc.SchedulerBase] = None,
    ):
        _scheduler = scheduler or scheduler_ or schedulers.NamedNewThreadScheduler(name="LunoWebsocket")
        connection: WebSocketApp | None = None

        def action(*args: Any):
            nonlocal connection

            def on_error(_ws: WebSocketApp, error: Exception):
                logger.error("[SOCKET][RAW] Websocket errored %s", error)
                observer.on_next((enhanced, message_types.WEBSOCKET_STATUS, status.WEBSOCKET_CLOSED))
                observer.on_error(error)

            def on_close(_ws: WebSocketApp, close_status_code: int, close_msg: str):
                logger.warning(
                    "[SOCKET][RAW] Websocket closed | url: %s, status: %s, close message: %s",
                    url,
                    close_status_code,
                    close_msg,
                )
                observer.on_next((enhanced, message_types.WEBSOCKET_STATUS, status.WEBSOCKET_CLOSED))
                observer.on_error(Exception('Socket closed'))

            def on_open(_ws: WebSocketApp):
                logger.info("[SOCKET][RAW] Websocket opened at %s", url)
                observer.on_next((enhanced, message_types.WEBSOCKET_STATUS, status.WEBSOCKET_OPENED))

            def on_message(_ws: WebSocketApp, message: bytes | str):
                pass_message = orjson.loads(message)
                category = message_types.WEBSOCKET_MESSAGE
                raw_logger.debug(message)
                if 'error_code' in pass_message:
                    observer.on_error(Exception(pass_message['error_message']))
                    return
                
                try:
                    observer.on_next((enhanced, category, pass_message))
                except:
                    logger.exception("[SOCKET] Error on socket message")

            connection = WebSocketApp(
                url,
                on_open=on_open,
                on_close=on_close,
                on_error=on_error,
                on_message=on_message,
            )
            enhanced = enhanced_websocket.EnhancedWebsocket(connection)

            def run_forever(*args: Any):
                assert connection is not None
                connection.run_forever()

            _scheduler.schedule(run_forever)

        def disconnect():
            logger.info("[SOCKET] Releasing resources")
            assert connection is not None
            try:
                connection.close()
            except WebSocketConnectionClosedException as exc:
                logger.error("[SOCKET] Socket was already closed %s", exc)

        return disposable.CompositeDisposable(
            _scheduler.schedule(action), disposable.Disposable(disconnect)
        )

    return observable.Observable(subscribe)
