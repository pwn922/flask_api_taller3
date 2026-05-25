from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync


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
        # TODO: implementar query
        # SELECT producto, SUM(precio) AS total
        # FROM ventas
        # WHERE ...
        # GROUP BY producto ORDER BY total DESC
        return []
