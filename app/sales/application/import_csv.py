import io

import pandas as pd

from app.db.starrocks.client import StarRocksClientAsync
from app.sales.application.errors import (
    EmptyFileError,
    InvalidColumnsError,
    InvalidCsvFormatError,
)
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS

BATCH_SIZE = 1000
CSV_COLUMNS = (
    "usuario_id, edad, ciudad, producto, categoria, precio, "
    "fecha, hora, metodo_pago"
)
EXPECTED_COLUMNS = [c.strip() for c in CSV_COLUMNS.split(",")]
PLACEHOLDERS = ", ".join(["%s"] * len(EXPECTED_COLUMNS))


class ImportCsvUseCase:
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def execute(self, csv_bytes: bytes, delete_existing: bool = False) -> dict:
        if delete_existing:
            await self.client.command(f"TRUNCATE TABLE {TABLE_NAME_VENTAS}")

        try:
            df = pd.read_csv(io.BytesIO(csv_bytes), encoding="utf-8")
        except Exception:
            raise InvalidCsvFormatError()

        if df.empty:
            raise EmptyFileError()

        actual_columns = [c.strip() for c in df.columns]
        if actual_columns != EXPECTED_COLUMNS:
            raise InvalidColumnsError()

        total = len(df)
        imported = 0
        errors = 0

        query = (
            f"INSERT INTO {TABLE_NAME_VENTAS} ({CSV_COLUMNS}) "
            f"VALUES ({PLACEHOLDERS})"
        )

        for i in range(0, total, BATCH_SIZE):
            batch = df.iloc[i : i + BATCH_SIZE]
            params_list = [
                tuple(
                    None if pd.isna(v) or v == "" or v == "\\N" else v
                    for v in row
                )
                for _, row in batch.iterrows()
            ]
            try:
                await self.client.executemany(query, params_list)
                imported += len(batch)
            except Exception:
                errors += len(batch)

        return {"imported": imported, "errors": errors, "total_lines": total}
