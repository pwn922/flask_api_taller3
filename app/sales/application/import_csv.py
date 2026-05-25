import asyncio
import base64
import json
import time
import urllib.request

from app.config import ActiveConfig
from app.db.starrocks.client import get_starrocks_client
from app.sales.infrastructure.databases.starrocks.models.sale_model import TABLE_NAME_VENTAS

STREAM_LOAD_COLUMNS = "usuario_id,edad,ciudad,producto,categoria,precio,fecha,hora,metodo_pago"


class ImportCsvUseCase:
    async def execute(self, csv_bytes: bytes, delete_existing: bool = False) -> dict:
        if delete_existing:
            client = await get_starrocks_client()
            await client.command(f"TRUNCATE TABLE {TABLE_NAME_VENTAS}")

        url = (
            f"http://{ActiveConfig.STARROCKS_HOST}:8040"
            f"/api/{ActiveConfig.STARROCKS_DATABASE}/{TABLE_NAME_VENTAS}/_stream_load"
        )

        label = f"import_{int(time.time() * 1000)}"

        credentials = base64.b64encode(
            f"{ActiveConfig.STARROCKS_USER}:{ActiveConfig.STARROCKS_PASSWORD}".encode()
        ).decode()

        # Strip header line so it's not imported as data
        first_newline = csv_bytes.find(b"\n")
        if first_newline != -1:
            csv_bytes = csv_bytes[first_newline + 1:]

        def _do_load():
            req = urllib.request.Request(url, data=csv_bytes, method="PUT")
            req.add_header("Expect", "100-continue")
            req.add_header("Content-Type", "text/plain; charset=UTF-8")
            req.add_header("label", label)
            req.add_header("columns", STREAM_LOAD_COLUMNS)
            req.add_header("column_separator", ",")
            req.add_header("Authorization", f"Basic {credentials}")

            with urllib.request.urlopen(req, timeout=600) as resp:
                return json.loads(resp.read().decode())

        result = await asyncio.to_thread(_do_load)

        status = result.get("Status", "Fail")
        imported = int(result.get("NumberLoadedRows", 0))
        errors = int(result.get("NumberFilteredRows", 0))

        if status != "Success":
            msg = result.get("Message", status)
            raise RuntimeError(f"Stream Load falló: {msg}")

        return {"imported": imported, "errors": errors, "total_lines": imported + errors}
