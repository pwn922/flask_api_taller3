from app.db.starrocks.client import StarRocksClientAsync
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS

BATCH_SIZE = 1000
CSV_COLUMNS = (
    "usuario_id, edad, ciudad, producto, categoria, precio, "
    "fecha, hora, metodo_pago"
)


class ImportCsvUseCase:
    def __init__(self, client: StarRocksClientAsync):
        self.client = client

    async def execute(self, csv_bytes: bytes, delete_existing: bool = False) -> dict:
        if delete_existing:
            await self.client.command(f"TRUNCATE TABLE {TABLE_NAME_VENTAS}")

        lines = csv_bytes.decode("utf-8").strip().splitlines()
        if not lines:
            return {"imported": 0, "errors": 0, "total_lines": 0}

        data_lines = lines[1:]
        total = len(data_lines)
        imported = 0
        errors = 0

        for i in range(0, total, BATCH_SIZE):
            batch = data_lines[i : i + BATCH_SIZE]
            values_sql = _build_values(batch)
            query = (
                f"INSERT INTO {TABLE_NAME_VENTAS} ({CSV_COLUMNS}) "
                f"VALUES {values_sql}"
            )
            try:
                await self.client.command(query)
                imported += len(batch)
            except Exception:
                errors += len(batch)

        return {"imported": imported, "errors": errors, "total_lines": total}


def _build_values(lines: list[str]) -> str:
    rows = []
    for line in lines:
        if not line.strip():
            continue
        cols = line.split(",")
        escaped = []
        for val in cols:
            v = val.strip()
            if v == "" or v == "\\N":
                escaped.append("NULL")
            else:
                safe = v.replace("'", "''")
                escaped.append(f"'{safe}'")
        rows.append("(" + ",".join(escaped) + ")")
    return ",".join(rows)
