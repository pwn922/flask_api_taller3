from typing import List, Dict, Any, Optional

from app.db.starrocks.client import StarRocksClientAsync
from app.sales.domain.sale import Sale, SaleRepository
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS


class StarRocksSaleRepository(SaleRepository):
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Sale]:
        return []
