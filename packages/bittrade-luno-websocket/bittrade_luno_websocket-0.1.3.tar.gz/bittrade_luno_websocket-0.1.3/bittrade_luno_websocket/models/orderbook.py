
from typing import TypedDict


class RawOrder(TypedDict):
    id: str
    price: str
    volume: str

class RawOrderBook(TypedDict):
    bids: list[RawOrder]
    asks: list[RawOrder]
    timestamp: int
