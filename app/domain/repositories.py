from __future__ import annotations

from abc import ABC, abstractmethod
from app.domain.models import Order


class OrderRepository(ABC):
    @abstractmethod
    def external_id_exists(self, external_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save_order(self, order: Order) -> int:
        """Guarda la orden y retorna el ID interno."""
        raise NotImplementedError

    @abstractmethod
    def customer_report(self) -> list[dict]:
        """Retorna el agregado por cliente."""
        raise NotImplementedError
