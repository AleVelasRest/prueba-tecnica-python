from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.domain.repositories import OrderRepository
from app.domain.models import Order
from app.domain.errors import InfrastructureError, ConflictError

from app.infra.sql_models import CustomerDB, OrderDB, OrderItemDB


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def external_id_exists(self, external_id: str) -> bool:
        try:
            q = select(func.count()).select_from(OrderDB).where(OrderDB.external_id == external_id)
            return self.session.execute(q).scalar_one() > 0
        except SQLAlchemyError as e:
            raise InfrastructureError(str(e)) from e

    def save_order(self, order: Order) -> int:
        try:
            customer = self.session.execute(
                select(CustomerDB).where(CustomerDB.email == order.customer.email)
            ).scalar_one_or_none()

            if customer is None:
                customer = CustomerDB(
                    email=order.customer.email,
                    name=order.customer.name,
                    client_id=order.customer.client_id,
                )
                self.session.add(customer)
                self.session.flush()

            order_db = OrderDB(
                external_id=order.external_id,
                customer_id=customer.id,
                date=order.date,
                total=order.total,
                is_vip=order.is_vip,
                arrival_date=order.arrival_date,
            )
            self.session.add(order_db)
            self.session.flush()

            for it in order.items:
                self.session.add(
                    OrderItemDB(
                        order_id=order_db.id,
                        sku=it.sku,
                        quantity=it.quantity,
                        price_unit=it.price_unit,
                    )
                )

            self.session.flush()
            return order_db.id

        except IntegrityError as e:
            # por si hay carrera con external_id único
            raise ConflictError("external_id ya existe") from e
        except SQLAlchemyError as e:
            raise InfrastructureError(str(e)) from e

    def customer_report(self) -> list[dict]:
        """
        Reporte acumulado por cliente:
        - total_orders: count(orders)
        - total_amount_spent: sum(total)
        - is_vip: (sum(total) > 300)
        - arrival_date: max(arrival_date)
        """
        try:
            rows = self.session.execute(
                select(
                    CustomerDB.email.label("customer_email"),
                    func.count(OrderDB.id).label("total_orders"),
                    func.coalesce(func.sum(OrderDB.total), 0.0).label("total_amount_spent"),
                    func.max(OrderDB.arrival_date).label("arrival_date"),
                )
                .join(OrderDB, OrderDB.customer_id == CustomerDB.id)
                .group_by(CustomerDB.email)
                .order_by(CustomerDB.email.asc())
            ).all()

            out: list[dict] = []
            for r in rows:
                total_spent = float(r.total_amount_spent)
                out.append(
                    {
                        "customer_email": r.customer_email,
                        "total_orders": int(r.total_orders),
                        "total_amount_spent": round(total_spent, 2),
                        "is_vip": str(total_spent > 300.0),
                        "arrival_date": r.arrival_date.isoformat() if r.arrival_date else None,
                    }
                )
            return out

        except SQLAlchemyError as e:
            raise InfrastructureError(str(e)) from e
