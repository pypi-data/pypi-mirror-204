import dataclasses
from typing import TypedDict


class Balance(TypedDict):
    account_id: str
    asset: str
    balance: str
    name: str
    reserved: str
    unconfirmed: str


@dataclasses.dataclass
class BalanceRequest:
    assets: list[str] = dataclasses.field(default_factory=list)

    def to_dict(self):
        if self.assets:
            return {"assets": self.assets}
        return {}


class BalanceResponse(TypedDict):
    balances: dict[str, Balance]
