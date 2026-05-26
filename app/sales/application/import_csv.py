import io
import logging
from typing import Optional

import pandas as pd

from app.db.starrocks.client import get_starrocks_client
from app.db.starrocks.stream_load_client import (
    StarRocksStreamLoadClient,
    StreamLoadResult,
)
from app.sales.application.errors import (
    EmptyFileError,
    InvalidColumnsError,
    InvalidCsvFormatError,
)
from app.sales.infrastructure.databases.starrocks.models.sale_model import (
    TABLE_NAME_VENTAS,
)

logger = logging.getLogger(__name__)

VALIDATION_ROWS = 100

CSV_COLUMNS = (
    "usuario_id, edad, ciudad, producto, categoria, precio, "
    "fecha, hora, metodo_pago"
)
EXPECTED_COLUMNS = [c.strip() for c in CSV_COLUMNS.split(",")]

COLUMN_ALIASES = {
    "usuarioid": "usuario_id",
    "metodopago": "metodo_pago",
}


class ImportCsvUseCase:
    def __init__(self):
        pass

    def _normalize_columns(self, columns: list[str]) -> list[str]:
        normalized = []
        for col in columns:
            col_clean = col.strip().lower()
            if col_clean in COLUMN_ALIASES:
                normalized.append(COLUMN_ALIASES[col_clean])
            else:
                normalized.append(col_clean)
        return normalized

    def _validate_csv_structure(
        self, csv_bytes: bytes
    ) -> tuple[bool, Optional[str], int]:
        try:
            buffer = io.BytesIO(csv_bytes)
            df_sample = pd.read_csv(
                buffer,
                nrows=VALIDATION_ROWS,
                encoding="utf-8",
                on_bad_lines="skip",
            )
        except Exception as e:
            logger.warning(f"CSV format validation failed: {e}")
            return False, "El archivo no es un CSV válido", 0

        if df_sample.empty:
            return False, "El archivo CSV está vacío", 0

        actual_columns = self._normalize_columns(list(df_sample.columns))

        if actual_columns != EXPECTED_COLUMNS:
            expected = ", ".join(EXPECTED_COLUMNS)
            actual = ", ".join(actual_columns)
            logger.warning(
                f"Column mismatch. Expected: [{expected}], Actual: [{actual}]"
            )
            return False, "Las columnas del CSV no coinciden con la estructura esperada", 0

        try:
            df_sample["precio"] = pd.to_numeric(df_sample["precio"], errors="raise")
        except Exception:
            return False, "La columna 'precio' debe contener valores numéricos", 0

        total_estimated = self._estimate_total_rows(csv_bytes, df_sample)

        return True, None, total_estimated

    def _estimate_total_rows(self, csv_bytes: bytes, df_sample: pd.DataFrame) -> int:
        sample_rows = len(df_sample)
        sample_bytes = len(df_sample.to_csv(index=False).encode("utf-8"))
        total_bytes = len(csv_bytes)

        if sample_bytes == 0 or sample_rows == 0:
            return 0

        rows_per_byte = sample_rows / sample_bytes
        estimated = int(total_bytes * rows_per_byte)

        return max(estimated, sample_rows)

    async def _stream_load(
        self, csv_bytes: bytes, truncate_before: bool
    ) -> StreamLoadResult:
        client = StarRocksStreamLoadClient()

        columns = ", ".join(EXPECTED_COLUMNS)

        return await client.load_csv(
            table_name=TABLE_NAME_VENTAS,
            csv_bytes=csv_bytes,
            columns=columns,
            truncate_before=truncate_before,
            column_separator=",",
            skip_header=1,
            trim_space=True,
            timeout=300,
        )

    async def execute(self, csv_bytes: bytes, delete_existing: bool = False) -> dict:
        total_lines = 0
        imported = 0
        errors = 0

        if not csv_bytes or len(csv_bytes) == 0:
            raise EmptyFileError()

        is_valid, error_msg, estimated_rows = self._validate_csv_structure(
            csv_bytes
        )

        if not is_valid:
            if error_msg == "El archivo CSV está vacío":
                raise EmptyFileError()
            else:
                raise InvalidColumnsError()

        total_lines = estimated_rows

        logger.info(
            f"CSV validation passed. Estimated rows: {total_lines}. "
            f"Starting import (truncate={delete_existing})"
        )

        if delete_existing:
            logger.info(f"Truncating table {TABLE_NAME_VENTAS}...")
            mysql_client = await get_starrocks_client()
            await mysql_client.command(f"TRUNCATE TABLE {TABLE_NAME_VENTAS}")
            logger.info(f"Table {TABLE_NAME_VENTAS} truncated successfully")

        try:
            result = await self._stream_load(csv_bytes, truncate_before=False)

            if result.is_success():
                imported = result.number_loaded_rows
                errors = result.number_filtered_rows
                total_lines = result.number_total_rows

                logger.info(
                    f"Stream Load completed: {imported} imported, "
                    f"{errors} filtered, {total_lines} total"
                )
            else:
                logger.error(
                    f"Stream Load failed: {result.status} - {result.message}"
                )
                errors = total_lines
                imported = 0

        except Exception as e:
            logger.error(f"Unexpected error during Stream Load: {e}", exc_info=True)
            errors = total_lines
            imported = 0

        return {
            "imported": imported,
            "errors": errors,
            "total_lines": total_lines,
        }
