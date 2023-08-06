import dataclasses
from typing import Any, Callable
import reactivex
import requests
from bittrade_luno_websocket.models.rest.order import (
    OrderRequest,
    MarketOrderRequest,
    OrderResponse,
)
from bittrade_luno_websocket.connection.http import prepare_request, send_request
from bittrade_luno_websocket.models import RequestMessage
from bittrade_luno_websocket.models import endpoints
from bittrade_luno_websocket.rest.get_order import get_order_http, GetOrderRequest
from reactivex import operators, compose


def create_order_http_factory(
    add_token: Callable,
) -> Callable[[OrderRequest], reactivex.Observable[Any]]:
    def create_order_http(request: OrderRequest) -> reactivex.Observable[OrderResponse]:
        params = request.to_dict()
        return send_request(
            add_token(
                prepare_request(
                    RequestMessage(
                        method="POST",
                        endpoint=endpoints.Endpoints.POST_MARKET_ORDER
                        if request.type == "market"
                        else endpoints.Endpoints.POST_LIMIT_ORDER,
                        params=params,
                    )
                )
            )
        )

    return create_order_http


def post_market_order_http(
    request: MarketOrderRequest, add_token: Callable
) -> reactivex.Observable[OrderResponse]:
    return send_request(
        add_token(
            prepare_request(
                RequestMessage(
                    method="POST",
                    endpoint=endpoints.Endpoints.POST_MARKET_ORDER,
                    params=dataclasses.asdict(request),
                )
            )
        )
    )


def load_order_details(add_token: Callable):
    return compose(
        operators.flat_map(
            lambda x: get_order_http(GetOrderRequest(id=x["order_id"]), add_token)
        ),
    )
