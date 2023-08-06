from typing import Literal, TypedDict
from dataclasses import dataclass

@dataclass
class GetOrderRequest:
    id: str = ""
    client_order_id: str = ""
    def to_dict(self) -> dict:
        if self.id and self.client_order_id:
            raise ValueError("Both id and client_order_id cannot be provided")
        elif self.id:
            return {"id": self.id}
        elif self.client_order_id:
            return {"client_order_id": self.client_order_id}
        else:
            raise ValueError("Either id or client_order_id must be provided")


class GetOrderResponse(TypedDict):
    base: str
    client_order_id: str
    completed_timestamp: str
    counter: str
    creation_timestamp: str
    expiration_timestamp: str
    fee_base: str
    fee_counter: str
    limit_price: str
    limit_volume: str
    order_id: str
    pair: str
    side: Literal["BUY", "SELL"]
    status: Literal["AWAITING", "PENDING", "COMPLETE"]
    stop_direction: Literal["ABOVE", "BELOW"]
    stop_price: str
    time_in_force: Literal["GTC", "IOC", "FOK"]
    type: Literal["LIMIT", "MARKET", "STOP_LIMIT"]