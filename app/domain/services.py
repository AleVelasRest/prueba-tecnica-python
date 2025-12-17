from __future__ import annotations

from datetime import timedelta

from app.domain.errors import ConflictError
from app.domain.models import Order, Customer, Item
from app.domain.repositories import OrderRepository

VIP_THRESHOLD = 300.0


class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, external_id: str, customer: Customer, items: list[Item], date):
        if self.repo.external_id_exists(external_id):
            raise ConflictError(f"external_id '{external_id}' ya existe")

        total = sum(i.line_total for i in items)
        is_vip = total > VIP_THRESHOLD
        arrival_date = date + timedelta(days=3 if is_vip else 5)

        order = Order(
            external_id=external_id,
            customer=customer,
            items=items,
            date=date,
            total=float(total),
            is_vip=is_vip,
            arrival_date=arrival_date,
        )
        order_id = self.repo.save_order(order)
        return order_id, order

    def report(self) -> list[dict]:
        return self.repo.customer_report()
