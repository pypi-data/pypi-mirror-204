from decimal import Decimal
import functools
import logging
from elm_framework_helpers.websockets.models import (
    bundle,
    EnhancedWebsocket,
    message_types,
    status,
)
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.operators import retry_with_delay
from typing import Any, Callable, Literal, Optional, TypedDict, cast
from bittrade_luno_websocket.connection import generic
from bittrade_luno_websocket.connection.authenticate import send_credentials_operator

import reactivex
from reactivex import (
    Observable,
    observable,
    abc,
    operators,
    disposable,
    observer,
    throw,
)
from reactivex.scheduler import ThreadPoolScheduler
from returns import result, maybe

logger = logging.getLogger(__name__)


class UserStreamMessage(TypedDict):
    type: Literal["order_status", "order_fill", "balance_update"]
    order_status_update: dict
    order_fill_update: dict
    balance_update: dict


def user_stream_connection(
    key: str, secret: str, stable_delay: int = 10
) -> Observable[bundle.WebsocketBundle]:
    def subscribe(observer, scheduler=None):
        bundles = generic.raw_websocket_connection(
            "wss://ws.luno.com/api/1/userstream"
        ).pipe(
            retry_with_delay.retry_with_delay(
                retry_with_delay.luno_delay(), reactivex.timer(stable_delay)
            ),
            operators.share(),
        )

        authentication_sub = bundles.pipe(
            send_credentials_operator(key, secret),
        ).subscribe()

        return disposable.CompositeDisposable(
            authentication_sub, bundles.subscribe(observer, scheduler=scheduler)
        )

    return Observable(subscribe)
