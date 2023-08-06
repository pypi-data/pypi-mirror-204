from os import getenv
from typing import Literal
import requests
import reactivex
from reactivex.disposable import Disposable
from reactivex.scheduler import CurrentThreadScheduler
from logging import getLogger
from bittrade_luno_websocket import models

MARKET_URL = getenv("LUNO_HTTP_MARKET_URL", "https://api.luno.com")
# USER_URL = getenv("LUNO_HTTP_USER_URL", "https://api.luno.com")

session = requests.Session()

logger = getLogger(__name__)


def prepare_request(message: models.RequestMessage) -> requests.models.Request:
    http_method = message.method
    kwargs = {}
    kwargs["params"] = message.params

    endpoint = message.endpoint.value
    if message.url_format_arguments:
        endpoint = endpoint.format(**message.url_format_arguments)

    return requests.Request(http_method, f"{MARKET_URL}{endpoint}", **kwargs)


def send_request(request: requests.models.Request) -> reactivex.Observable:
    def subscribe(
        observer: reactivex.abc.ObserverBase,
        scheduler: reactivex.abc.SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        scheduler_ = scheduler or CurrentThreadScheduler()

        def act(s, state):
            del state, s  # Unused
            response = session.send(request.prepare())
            if response.ok:
                body = response.json()
                if "error_code" in body:
                    observer.on_error(body["error_code"])
                else:
                    observer.on_next(body)
                    observer.on_completed()
            else:
                try:
                    headers = response.request.headers
                    headers.pop("Authorization", None)
                    logger.error(
                        "Error with request %s; request was %s",
                        response.text,
                        response.request.body
                        if request.method == "POST"
                        else response.request.headers,
                    )
                    observer.on_error(str(response.status_code))
                except Exception as exc:
                    observer.on_error(exc)

        return scheduler_.schedule(act)

    return reactivex.Observable(subscribe)
