from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, Boolean, ForeignKey, UniqueConstraint
from datetime import datetime


class Base(DeclarativeBase):
    pass


class CustomerDB(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    client_id: Mapped[str] = mapped_column(String, nullable=False)

    orders: Mapped[list["OrderDB"]] = relationship(back_populates="customer")


class OrderDB(Base):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("external_id", name="uq_orders_external_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)

    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    is_vip: Mapped[bool] = mapped_column(Boolean, nullable=False)
    arrival_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    customer: Mapped["CustomerDB"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItemDB"]] = relationship(back_populates="order", cascade="all, delete-orphan")


class OrderItemDB(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True)

    sku: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_unit: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped["OrderDB"] = relationship(back_populates="items")
