from app.db.starrocks.client import StarRocksClientAsync
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS


class GetMetodosPagoListUseCase:
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def execute(self) -> list[str]:
        result = await self.client.execute(f"""
            SELECT DISTINCT metodo_pago
            FROM {TABLE_NAME_VENTAS}
            ORDER BY metodo_pago
        """)

        return [row[0] for row in result]
