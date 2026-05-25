from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync
from app.db.starrocks.filter_builder import SQLFilterBuilder
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS


class GetVentasPorFechaUseCase:
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

        result = await self.client.execute(f"""
            SELECT fecha, COUNT(*) AS total
            FROM {TABLE_NAME_VENTAS}
            {where}
            GROUP BY fecha
            ORDER BY fecha
        """, params)

        return [
            {"date": row[0].isoformat() if hasattr(row[0], 'isoformat') else str(row[0]), "total": int(row[1]) if row[1] is not None else 0}
            for row in result if row[0] is not None
        ]
