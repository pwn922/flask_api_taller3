from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync
from app.db.starrocks.filter_builder import SQLFilterBuilder
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS


class GetMetodosPagoUseCase:
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def execute(
        self,
        city: Optional[str] = None,
        category: Optional[str] = None,
        date_from: Optional[str] = None,
        date_until: Optional[str] = None,
    ) -> list[dict]:
        where, params = SQLFilterBuilder(
            city=city,
            category=category,
            date_from=date_from,
            date_until=date_until,
        ).build()

        result = await self.client.execute(f"""
            SELECT metodo_pago, COUNT(*) AS total
            FROM {TABLE_NAME_VENTAS}
            {where}
            GROUP BY metodo_pago
            ORDER BY total DESC
        """, params)

        return [
            {"payment_method": row[0], "total": int(row[1])}
            for row in result
        ]
