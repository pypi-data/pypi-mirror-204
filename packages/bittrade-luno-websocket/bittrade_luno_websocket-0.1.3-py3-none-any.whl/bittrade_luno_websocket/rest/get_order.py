from typing import Callable
from bittrade_luno_websocket.models.rest.get_order import GetOrderRequest, GetOrderResponse
from bittrade_luno_websocket.connection.http import prepare_request, send_request
from bittrade_luno_websocket.models import RequestMessage
from bittrade_luno_websocket.models import endpoints
import reactivex

def get_order_http(request: GetOrderRequest, add_token: Callable) -> reactivex.Observable[GetOrderResponse]:
    return send_request(add_token(prepare_request(RequestMessage(
        method="GET",
        endpoint=endpoints.Endpoints.GET_ORDER_V3,
        params=request.to_dict(),
    ))))