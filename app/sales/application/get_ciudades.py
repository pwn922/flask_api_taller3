from app.db.starrocks.client import StarRocksClientAsync
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS


class GetCiudadesUseCase:
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def execute(self) -> list[str]:
        result = await self.client.execute(f"""
            SELECT DISTINCT ciudad
            FROM {TABLE_NAME_VENTAS}
            ORDER BY ciudad
        """)

        return [row[0] for row in result]
