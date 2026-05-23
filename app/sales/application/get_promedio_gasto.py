from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync
from app.db.starrocks.filter_builder import SQLFilterBuilder
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS


class GetPromedioGastoUseCase:
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def execute(
        self,
        city: Optional[str] = None,
        category: Optional[str] = None,
        payment_method: Optional[str] = None,
        date_from: Optional[str] = None,
        date_until: Optional[str] = None,
    ) -> dict:
        where, params = SQLFilterBuilder(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from,
            date_until=date_until,
        ).build()

        query = f"SELECT AVG(precio) FROM {TABLE_NAME_VENTAS} {where}"

        result = await self.client.execute(query, params)
        promedio = float(result[0][0]) if result and result[0][0] else 0
        return {"promedio_gasto": promedio}
