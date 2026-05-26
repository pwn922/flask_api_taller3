from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync
from app.db.starrocks.filter_builder import SQLFilterBuilder
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS


class GetProductosMasVendidosUseCase:
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def execute(
        self,
        city: Optional[str] = None,
        category: Optional[str] = None,
        payment_method: Optional[str] = None,
        date_from: Optional[str] = None,
        date_until: Optional[str] = None,
    ) -> list[dict]:
        where, params = SQLFilterBuilder(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from,
            date_until=date_until,
        ).build()

        query = f"""
            SELECT producto, SUM(precio) AS total
            FROM {TABLE_NAME_VENTAS}
            {where}
            GROUP BY producto
            ORDER BY total DESC
            LIMIT 10
        """

        result = await self.client.execute(query, params)

        return [
            {"product": row[0], "total": float(row[1])}
            for row in result
        ]
