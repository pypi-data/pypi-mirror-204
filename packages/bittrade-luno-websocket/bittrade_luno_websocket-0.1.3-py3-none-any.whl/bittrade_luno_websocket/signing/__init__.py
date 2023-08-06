import requests.models
from requests.auth import HTTPBasicAuth
from logging import getLogger

logger = getLogger(__name__)

def add_http_token_factory(api_key: str, secret: str):
    def add_http_token(request: requests.models.Request) -> requests.models.Request:
        request.auth = HTTPBasicAuth(api_key, secret)
        return request

    return add_http_token