from datetime import date
from fastapi import APIRouter, File, Form, UploadFile
from typing import Optional

from app.db.starrocks.client import get_starrocks_client
from app.sales.application import (
    GetTotalVentasUseCase,
    GetPromedioGastoUseCase,
    GetProductoMasVendidoUseCase,
    GetCiudadMasCompradaUseCase,
    GetMetodoPagoMasUsadoUseCase,
    ImportCsvUseCase,
)
from app.sales.application.get_top_category import GetTopCategoryUseCase
from app.sales.application.get_ventas_por_categoria import GetVentasPorCategoriaUseCase
from app.sales.presentation.dto.api_response import ApiResponse

router = APIRouter()


@router.get("/total-ventas")
async def get_total_ventas(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetTotalVentasUseCase(client)

        date_from_iso = date_from.isoformat() if date_from else None
        date_until_iso = date_until.isoformat() if date_until else None

        result = await use_case.execute(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from_iso,
            date_until=date_until_iso
        )

        total = result["total_ventas"]

        return ApiResponse(
            success=True,
            message="Total de ventas calculado correctamente" if total else "No hay ventas registradas",
            data={"total_ventas": total},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al calcular el total de ventas. Intente nuevamente.",
            data={"total_ventas": 0},
        )


@router.get("/promedio-gasto")
async def get_promedio_gasto(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetPromedioGastoUseCase(client)

        date_from_iso = date_from.isoformat() if date_from else None
        date_until_iso = date_until.isoformat() if date_until else None

        result = await use_case.execute(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from_iso,
            date_until=date_until_iso,
        )

        promedio = result["promedio_gasto"]

        return ApiResponse(
            success=True,
            message="Promedio de gasto calculado correctamente" if promedio else "No hay ventas registradas",
            data={"promedio_gasto": promedio},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al calcular el promedio de gasto. Intente nuevamente.",
            data={"promedio_gasto": 0},
        )

@router.get("/top-category")
async def get_top_category(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetTopCategoryUseCase(client)

        date_from_iso = date_from.isoformat() if date_from else None
        date_until_iso = date_until.isoformat() if date_until else None

        result = await use_case.execute(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from_iso,
            date_until=date_until_iso,
        )

        if not result:
            return ApiResponse(
                success=True,
                message="No hay ventas registradas",
                data={"categories": []},
            )

        return ApiResponse(
            success=True,
            message="Categoría(s) más vendida(s) obtenida(s) correctamente",
            data={"categories": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener la categoría más vendida. Intente nuevamente.",
            data={"categories": []},
        )

@router.get("/ventas-por-categoria")
async def get_ventas_por_categoria(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetVentasPorCategoriaUseCase(client)

        date_from_iso = date_from.isoformat() if date_from else None
        date_until_iso = date_until.isoformat() if date_until else None

        result = await use_case.execute(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from_iso,
            date_until=date_until_iso,
        )

        if not result:
            return ApiResponse(
                success=True,
                message="No hay ventas registradas",
                data={"categories": []},
            )

        return ApiResponse(
            success=True,
            message="Ventas por categoría obtenidas correctamente",
            data={"categories": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener ventas por categoría. Intente nuevamente.",
            data={"categories": []},
        )


@router.get("/producto-mas-vendido")
async def get_producto_mas_vendido(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetProductoMasVendidoUseCase(client)

        date_from_iso = date_from.isoformat() if date_from else None
        date_until_iso = date_until.isoformat() if date_until else None

        result = await use_case.execute(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from_iso,
            date_until=date_until_iso,
        )

        if not result:
            return ApiResponse(
                success=True,
                message="No hay ventas registradas",
                data={"products": []},
            )

        return ApiResponse(
            success=True,
            message="Producto(s) más vendido(s) obtenido(s) correctamente",
            data={"products": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener el producto más vendido. Intente nuevamente.",
            data={"products": []},
        )


@router.get("/ciudad-mas-comprada")
async def get_ciudad_mas_comprada(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetCiudadMasCompradaUseCase(client)

        date_from_iso = date_from.isoformat() if date_from else None
        date_until_iso = date_until.isoformat() if date_until else None

        result = await use_case.execute(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from_iso,
            date_until=date_until_iso,
        )

        if not result:
            return ApiResponse(
                success=True,
                message="No hay ventas registradas",
                data={"cities": []},
            )

        return ApiResponse(
            success=True,
            message="Ciudad(es) más comprada(s) obtenida(s) correctamente",
            data={"cities": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener la ciudad más comprada. Intente nuevamente.",
            data={"cities": []},
        )


@router.get("/metodo-pago-mas-usado")
async def get_metodo_pago_mas_usado(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetMetodoPagoMasUsadoUseCase(client)

        date_from_iso = date_from.isoformat() if date_from else None
        date_until_iso = date_until.isoformat() if date_until else None

        result = await use_case.execute(
            city=city,
            category=category,
            payment_method=payment_method,
            date_from=date_from_iso,
            date_until=date_until_iso,
        )

        if not result:
            return ApiResponse(
                success=True,
                message="No hay ventas registradas",
                data={"payment_methods": []},
            )

        return ApiResponse(
            success=True,
            message="Método(s) de pago más usado(s) obtenido(s) correctamente",
            data={"payment_methods": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener el método de pago más usado. Intente nuevamente.",
            data={"payment_methods": []},
        )


@router.post("/import-csv")
async def import_csv(
    file: UploadFile = File(...),
    delete_existing: bool = Form(False),
):
    try:
        use_case = ImportCsvUseCase()

        csv_bytes = await file.read()
        result = await use_case.execute(csv_bytes, delete_existing=delete_existing)

        return ApiResponse(
            success=True,
            message=f"Se importaron {result['imported']} registros correctamente"
                    + (f" ({result['errors']} errores)" if result['errors'] else ""),
            data=result,
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            message=f"Error al importar CSV: {str(e)}",
            data={"imported": 0, "errors": 0},
        )
