from typing import Optional

from app.db.starrocks.client import StarRocksClientAsync


class GetMetodosPagoUseCase:
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
        # SELECT metodo_pago, COUNT(*) AS total
        # FROM ventas
        # WHERE ...
        # GROUP BY metodo_pago ORDER BY total DESC
        return []
