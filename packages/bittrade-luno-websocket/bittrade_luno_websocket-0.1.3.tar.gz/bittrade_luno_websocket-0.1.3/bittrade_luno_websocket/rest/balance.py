import dataclasses
from typing import Any, Callable
import reactivex
import requests
from bittrade_luno_websocket.models.rest.balance import BalanceRequest, BalanceResponse
from bittrade_luno_websocket.connection.http import prepare_request, send_request
from bittrade_luno_websocket.models import RequestMessage
from bittrade_luno_websocket.models import endpoints


def load_balances_http_factory(
    add_token: Callable,
) -> Callable[[BalanceRequest], reactivex.Observable[BalanceResponse]]:
    def load_balances_http(
        request: BalanceRequest | None = None,
    ) -> reactivex.Observable[BalanceResponse]:
        params = request.to_dict() if request else {}
        return send_request(
            add_token(
                prepare_request(
                    RequestMessage(
                        method="GET",
                        endpoint=endpoints.Endpoints.GET_BALANCES,
                        params=params,
                    )
                )
            )
        )

    return load_balances_http
