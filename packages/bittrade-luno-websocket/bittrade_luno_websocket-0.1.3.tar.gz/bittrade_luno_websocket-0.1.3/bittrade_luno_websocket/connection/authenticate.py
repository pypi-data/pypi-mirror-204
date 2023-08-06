from typing import Any, Callable
import reactivex
from reactivex import abc, observable
from elm_framework_helpers.websockets.models import bundle, EnhancedWebsocket
import logging

logger = logging.getLogger(__name__)

def send_credentials_operator(api_key: str, secret: str) -> Callable[[observable.Observable[bundle.WebsocketBundle]], observable.Observable[bundle.WebsocketBundle]]:
    previous_websocket: EnhancedWebsocket | None = None

    def send_credentials(source: observable.Observable[bundle.WebsocketBundle]) -> observable.Observable[bundle.WebsocketBundle]:
        def subscribe(observer: abc.ObserverBase, scheduler: abc.SchedulerBase) -> abc.DisposableBase:
            def on_next(message: bundle.WebsocketBundle) -> None:
                nonlocal previous_websocket

                if previous_websocket != message[0]:
                    previous_websocket = message[0]

                    logger.info('Websocket connected; sending credentials')
                    message[0].send_json({
                        "api_key_id": api_key,
                        "api_key_secret": secret
                    })
                
                observer.on_next(message)

            return source.subscribe(on_next, observer.on_error, observer.on_completed, scheduler=scheduler)
        return observable.Observable(subscribe)
    return send_credentials