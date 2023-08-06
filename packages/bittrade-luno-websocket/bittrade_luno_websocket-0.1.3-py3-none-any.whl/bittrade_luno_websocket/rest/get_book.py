import requests
from reactivex import observable
from bittrade_luno_websocket.models.orderbook import RawOrderBook
from bittrade_luno_websocket.connection.http import send_request, prepare_request
from bittrade_luno_websocket.models import RequestMessage, endpoints
from reactivex import abc

def load_order_book_http(symbol: str) -> observable.Observable[RawOrderBook]:
    return send_request(
        prepare_request(RequestMessage(
            method="GET",
            endpoint=endpoints.Endpoints.ORDERBOOK_TOP,
            params={"pair": symbol.upper()},
        ))
    )
