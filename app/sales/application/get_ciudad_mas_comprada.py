from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync
from app.db.starrocks.filter_builder import SQLFilterBuilder
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS


class GetCiudadMasCompradaUseCase:
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def execute(
        self,
        category: Optional[str] = None,
        payment_method: Optional[str] = None,
        date_from: Optional[str] = None,
        date_until: Optional[str] = None,
    ) -> list[dict] | None:
        where, params = SQLFilterBuilder(
            category=category,
            payment_method=payment_method,
            date_from=date_from,
            date_until=date_until,
        ).build()

        result = await self.client.execute(f"""
            SELECT ciudad, total
            FROM (
                SELECT
                    ciudad,
                    COUNT(*) AS total,
                    RANK() OVER (ORDER BY COUNT(*) DESC) AS rnk
                FROM {TABLE_NAME_VENTAS}
                {where}
                GROUP BY ciudad
            ) t
            WHERE rnk = 1
            ORDER BY ciudad
        """, params)

        return [
            {"city": row[0], "total": int(row[1])}
            for row in result
        ] if result else None
