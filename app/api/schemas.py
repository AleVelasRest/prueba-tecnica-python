from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, conint, confloat


class CustomerIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1)
    client_id: str = Field(min_length=1)


class ItemIn(BaseModel):
    sku: str = Field(min_length=1)
    quantity: conint(gt=0)  # quantity > 0
    price_unit: confloat(ge=0)  # price_unit >= 0


class OrderIn(BaseModel):
    external_id: str = Field(min_length=1)
    customer: CustomerIn
    items: list[ItemIn] = Field(min_length=1)
    date: datetime


class OrderCreatedOut(BaseModel):
    id: int
    external_id: str
    total: float
    is_vip: bool
    arrival_date: datetime


class ReportRowOut(BaseModel):
    customer_email: str
    total_orders: int
    total_amount_spent: float
    is_vip: str
    arrival_date: str | None
