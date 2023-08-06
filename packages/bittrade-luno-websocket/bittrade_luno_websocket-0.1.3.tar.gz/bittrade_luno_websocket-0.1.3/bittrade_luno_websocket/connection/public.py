from bittrade_luno_websocket.connection import generic
from bittrade_luno_websocket.connection.authenticate import send_credentials_operator
from elm_framework_helpers.operators import retry_with_delay
import reactivex
import os


MARKET_URL = os.getenv(
    "LUNO_MARKET_URL", "wss://ws.luno.com/api/1/stream"
)



def public_connection(api_key: str, secret: str, *, orderbook_symbol: str = ""):
    url = MARKET_URL
    if orderbook_symbol:
        url = f"{MARKET_URL}/{orderbook_symbol}"
    return generic.raw_websocket_connection(url).pipe(
        send_credentials_operator(api_key, secret),
        retry_with_delay.retry_with_delay(
            retry_with_delay.luno_delay(), reactivex.timer(30)
        )
    )