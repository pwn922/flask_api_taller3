import aiomysql
import logging
from typing import Optional, List, Tuple, Any, Sequence
from app.config import ActiveConfig

logger = logging.getLogger(__name__)

class StarRocksClientAsync:
    def __init__(self):
        self.pool: Optional[aiomysql.Pool] = None

    async def connect(self) -> "StarRocksClientAsync":
        if self.pool is not None:
            return self

        try:
            self.pool = await aiomysql.create_pool(
                host=ActiveConfig.STARROCKS_HOST,
                port=int(ActiveConfig.STARROCKS_PORT),
                db=ActiveConfig.STARROCKS_DATABASE,
                user=ActiveConfig.STARROCKS_USER,
                password=ActiveConfig.STARROCKS_PASSWORD,
                autocommit=True,
                minsize=2,
                maxsize=10,
            )
            return self
        except Exception as e:
            logger.error(f"Error al conectar con StarRocks: {e}")
            raise

    async def _get_connection(self):
        if not self.pool:
            raise RuntimeError("El cliente no está conectado. Llame a 'await connect()' primero.")
        return self.pool.acquire()

    async def execute(self, query: str, parameters: Optional[tuple] = None) -> List[Tuple[Any, ...]]:
        async with await self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, parameters)
                return await cursor.fetchall()

    async def command(self, query: str, parameters: Optional[tuple] = None) -> None:
        async with await self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, parameters)

    async def executemany(self, query: str, parameters: List[Tuple[Any, ...]]) -> None:
        async with await self._get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.executemany(query, parameters)

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None


_starrocks_client: Optional[StarRocksClientAsync] = None

async def get_starrocks_client() -> StarRocksClientAsync:
    global _starrocks_client
    if _starrocks_client is None:
        client = StarRocksClientAsync()
        _starrocks_client = await client.connect()
    return _starrocks_client
