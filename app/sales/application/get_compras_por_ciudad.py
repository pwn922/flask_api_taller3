from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync


class GetComprasPorCiudadUseCase:
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
        # SELECT ciudad, COUNT(*) AS total
        # FROM ventas
        # WHERE ...
        # GROUP BY ciudad ORDER BY total DESC
        return []
