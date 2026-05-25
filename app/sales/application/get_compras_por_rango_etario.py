from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync


class GetComprasPorRangoEtarioUseCase:
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
        # SELECT CASE
        #   WHEN edad BETWEEN 18 AND 25 THEN '18-25'
        #   WHEN edad BETWEEN 26 AND 35 THEN '26-35'
        #   ...
        # END AS rango, COUNT(*) AS total
        # FROM ventas
        # WHERE ...
        # GROUP BY rango ORDER BY rango
        return []
