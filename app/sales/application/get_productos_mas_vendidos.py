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
        limit: int = 10,
    ) -> list[dict]:
        where, params = SQLFilterBuilder(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from,
            date_until=date_until,
        ).build()

        query = f"""
            SELECT producto, COUNT(*) AS total
            FROM {TABLE_NAME_VENTAS}
            {where}
            GROUP BY producto
            ORDER BY total DESC
            LIMIT %s
        """

        result = await self.client.execute(query, (*params, limit))

        return [
            {"product": row[0], "total": int(row[1]) if row[1] is not None else 0}
            for row in result if row[0] is not None
        ]
