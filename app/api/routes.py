from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.domain.services import OrderService
from app.domain.models import Customer, Item
from app.domain.errors import DomainError
from app.infra.sql_repositories import SqlAlchemyOrderRepository
from app.api.schemas import OrderIn, OrderCreatedOut, ReportRowOut


router = APIRouter()


def session_dep():
    with get_session() as s:
        yield s


@router.post("/orders", response_model=OrderCreatedOut, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderIn, session: Session = Depends(session_dep)):
    repo = SqlAlchemyOrderRepository(session)
    service = OrderService(repo)

    customer = Customer(
        email=str(payload.customer.email),
        name=payload.customer.name,
        client_id=payload.customer.client_id,
    )
    items = [Item(sku=i.sku, quantity=i.quantity, price_unit=float(i.price_unit)) for i in payload.items]

    order_id, order = service.create_order(
        external_id=payload.external_id,
        customer=customer,
        items=items,
        date=payload.date,
    )

    return OrderCreatedOut(
        id=order_id,
        external_id=order.external_id,
        total=round(order.total, 2),
        is_vip=order.is_vip,
        arrival_date=order.arrival_date,
    )


@router.get("/orders/report", response_model=list[ReportRowOut])
def report(session: Session = Depends(session_dep)):
    repo = SqlAlchemyOrderRepository(session)
    service = OrderService(repo)
    return service.report()
