from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Customer:
    email: str
    name: str
    client_id: str


@dataclass(frozen=True)
class Item:
    sku: str
    quantity: int
    price_unit: float

    @property
    def line_total(self) -> float:
        return float(self.quantity) * float(self.price_unit)


@dataclass(frozen=True)
class Order:
    external_id: str
    customer: Customer
    items: list[Item]
    date: datetime
    total: float
    is_vip: bool
    arrival_date: datetime
