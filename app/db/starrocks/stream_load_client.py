import base64
import logging
from typing import Optional, AsyncGenerator, Dict, Any, BinaryIO

import httpx
from app.config import ActiveConfig

logger = logging.getLogger(__name__)


class StreamLoadResult:
    def __init__(self, data: Dict[str, Any]):
        self.status = data.get("Status", "Unknown")
        self.message = data.get("Message", "")
        self.number_total_rows = int(data.get("NumberTotalRows", 0))
        self.number_loaded_rows = int(data.get("NumberLoadedRows", 0))
        self.number_filtered_rows = int(data.get("NumberFilteredRows", 0))
        self.number_unselected_rows = int(data.get("NumberUnselectedRows", 0))
        self.load_bytes = int(data.get("LoadBytes", 0))
        self.load_time_ms = int(data.get("LoadTimeMs", 0))
        self.error_url = data.get("ErrorURL", "")
        self.raw = data

    def is_success(self) -> bool:
        return self.status == "Success"

    def __str__(self) -> str:
        return (
            f"StreamLoadResult(status={self.status}, "
            f"loaded={self.number_loaded_rows}/{self.number_total_rows}, "
            f"time={self.load_time_ms}ms)"
        )


class StarRocksStreamLoadClient:
    def __init__(
        self,
        host: Optional[str] = None,
        http_port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.host = host or ActiveConfig.STARROCKS_HOST
        self.http_port = http_port or ActiveConfig.STARROCKS_HTTP_PORT
        self.database = database or ActiveConfig.STARROCKS_DATABASE
        self.user = user or ActiveConfig.STARROCKS_USER
        self.password = password or ActiveConfig.STARROCKS_PASSWORD

        self._auth_header = self._build_auth_header()

    def _build_auth_header(self) -> str:
        credentials = f"{self.user}:{self.password}"
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return f"Basic {encoded}"

    def _build_url(self, table_name: str) -> str:
        return (
            f"http://{self.host}:{self.http_port}"
            f"/api/{self.database}/{table_name}/_stream_load"
        )

    @staticmethod
    def _chunk_generator(
        file_like: BinaryIO, chunk_size: int = 8192 * 1024
    ) -> AsyncGenerator[bytes, None]:
        while True:
            chunk = file_like.read(chunk_size)
            if not chunk:
                break
            yield chunk

    async def load_csv(
        self,
        table_name: str,
        csv_bytes: bytes,
        columns: str,
        column_mapping: Optional[str] = None,
        truncate_before: bool = False,
        column_separator: str = ",",
        skip_header: int = 1,
        trim_space: bool = True,
        timeout: int = 300,
    ) -> StreamLoadResult:
        headers = {
            "Authorization": self._auth_header,
            "columns": columns,
            "column_separator": column_separator,
            "skip_header": str(skip_header),
            "trim_space": str(trim_space).lower(),
            "format": "csv",
        }

        if column_mapping:
            headers["column_mapping"] = column_mapping

        if truncate_before:
            headers["truncate"] = "true"

        url = self._build_url(table_name)

        logger.info(
            f"Starting Stream Load to {self.database}.{table_name} "
            f"(truncate={truncate_before})"
        )

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.put(
                url,
                content=csv_bytes,
                headers=headers,
            )

        result = StreamLoadResult(response.json())

        if result.is_success():
            logger.info(f"Stream Load successful: {result}")
        else:
            logger.error(
                f"Stream Load failed: {result.status} - {result.message}. "
                f"ErrorURL: {result.error_url}"
            )

        return result
