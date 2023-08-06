from dataclasses import dataclass
import dataclasses
from typing import Literal, TypedDict


@dataclass
class OrderRequest:
    type: Literal["market", "limit"]
    side: Literal["buy", "sell"]
    volume: str
    pair: str
    price: str = ""
    post_only: bool = False
    time_in_force: str = "GTC"
    stop_price: str = ""
    stop_direction: str = ""
    client_order_id: str = ""

    def to_dict(self):
        side = self.side
        as_dict = {
            "pair": self.pair,
        }
        if self.type == "market":
            as_dict["type"] = side.upper()
            as_dict["counter_volume" if side == "buy" else "base_volume"] = self.volume
        else:
            as_dict["volume"] = self.volume
            as_dict["price"] = self.price
            as_dict["type"] = "BID" if (side == "buy") else "ASK"
            if self.post_only:
                as_dict["post_only"] = True
        return as_dict


class OrderResponse(TypedDict):
    order_id: str


@dataclass
class MarketOrderRequest:
    pair: str
    type: str
    base_account_id: int
    counter_account_id: int
    base_volume: str = None
    counter_volume: str = None
    timestamp: int = None
    ttl: int = 10000
    client_order_id: str = None
