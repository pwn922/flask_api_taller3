from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, time
from typing import Optional, Dict, Any, List


@dataclass
class Sale:
    usuario_id: int
    edad: int
    ciudad: str
    producto: str
    categoria: str
    precio: float
    fecha: date
    hora: time
    metodo_pago: str


class SaleRepository(ABC):
    @abstractmethod
    async def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Sale]:
        pass

    @abstractmethod
    async def create(self, sale: Sale) -> None:
        pass

    @abstractmethod
    async def create_many(self, sales: List[Sale]) -> None:
        pass

    @abstractmethod
    async def delete_all(self) -> None:
        pass
