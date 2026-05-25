from typing import List, Dict, Any, Optional
from datetime import date, time

from app.db.starrocks.client import StarRocksClientAsync
from app.sales.domain.sale import Sale, SaleRepository
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS, COLUMNS


class StarRocksSaleRepository(SaleRepository):
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Sale]:
        return []

    async def create(self, sale: Sale) -> None:
        query = f"""
            INSERT INTO {TABLE_NAME_VENTAS}
            ({", ".join(COLUMNS)})
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await self.client.command(query, (
            sale.usuario_id,
            sale.edad,
            sale.ciudad,
            sale.producto,
            sale.categoria,
            sale.precio,
            sale.fecha.isoformat(),
            sale.hora.strftime("%H:%M:%S"),
            sale.metodo_pago,
        ))

    async def delete_all(self) -> None:
        await self.client.command(f"TRUNCATE TABLE {TABLE_NAME_VENTAS}")

    async def create_many(self, sales: List[Sale]) -> int:
        batch_size = 1000
        total = 0
        for i in range(0, len(sales), batch_size):
            batch = sales[i:i + batch_size]

            placeholders = ", ".join(["(%s, %s, %s, %s, %s, %s, %s, %s, %s)"] * len(batch))
            query = f"""
                INSERT INTO {TABLE_NAME_VENTAS}
                ({", ".join(COLUMNS)})
                VALUES {placeholders}
            """

            params = []
            for sale in batch:
                params.extend([
                    sale.usuario_id,
                    sale.edad,
                    sale.ciudad,
                    sale.producto,
                    sale.categoria,
                    sale.precio,
                    sale.fecha.isoformat(),
                    sale.hora.strftime("%H:%M:%S"),
                    sale.metodo_pago,
                ])

            await self.client.command(query, tuple(params))
            total += len(batch)

        return total
