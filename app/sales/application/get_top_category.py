from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync
from app.db.starrocks.filter_builder import SQLFilterBuilder
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS


class GetTopCategoryUseCase:
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def execute(
        self,
        city: Optional[str] = None,
        payment_method: Optional[str] = None,
        date_from: Optional[str] = None,
        date_until: Optional[str] = None,
    ) -> list[dict] | None:
        where, params = SQLFilterBuilder(
            city=city,
            payment_method=payment_method,
            date_from=date_from,
            date_until=date_until,
        ).build()

        result = await self.client.execute(f"""
            SELECT categoria, total
            FROM (
                SELECT
                    categoria,
                    SUM(precio) AS total,
                    RANK() OVER (ORDER BY SUM(precio) DESC) AS rnk
                FROM {TABLE_NAME_VENTAS}
                {where}
                GROUP BY categoria
            ) t
            WHERE rnk = 1
            ORDER BY categoria
        """, params)

        return [
            {"category": row[0], "total": float(row[1])}
            for row in result
        ] if result else None
