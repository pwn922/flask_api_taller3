from datetime import date
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from typing import Optional

from app.db.starrocks.client import get_starrocks_client
from app.sales.application import (
    GetCategoriasUseCase,
    GetCiudadesUseCase,
    GetMetodosPagoListUseCase,
    GetTotalVentasUseCase,
    GetPromedioGastoUseCase,
    GetProductoMasVendidoUseCase,
    GetCiudadMasCompradaUseCase,
    GetMetodoPagoMasUsadoUseCase,
    ImportCsvUseCase,
)
from app.sales.application.get_top_category import GetTopCategoryUseCase
from app.sales.application.get_ventas_por_categoria import GetVentasPorCategoriaUseCase
from app.sales.application.get_compras_por_ciudad import GetComprasPorCiudadUseCase
from app.sales.application.get_compras_por_rango_etario import GetComprasPorRangoEtarioUseCase
from app.sales.application.get_ventas_por_fecha import GetVentasPorFechaUseCase
from app.sales.application.get_productos_mas_vendidos import GetProductosMasVendidosUseCase
from app.sales.application.get_metodos_pago import GetMetodosPagoUseCase
from app.sales.application.get_metodos_pago_mas_usados import GetMetodosPagoMasUsadosUseCase
from app.sales.application.errors import ImportCsvError
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


@router.get("/compras-por-ciudad")
async def get_compras_por_ciudad(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetComprasPorCiudadUseCase(client)

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
            message="Compras por ciudad obtenidas correctamente",
            data={"cities": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener compras por ciudad. Intente nuevamente.",
            data={"cities": []},
        )


@router.get("/compras-por-rango-etario")
async def get_compras_por_rango_etario(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetComprasPorRangoEtarioUseCase(client)

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
                data={"age_ranges": []},
            )

        return ApiResponse(
            success=True,
            message="Compras por rango etario obtenidas correctamente",
            data={"age_ranges": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener compras por rango etario. Intente nuevamente.",
            data={"age_ranges": []},
        )


@router.get("/ventas-por-fecha")
async def get_ventas_por_fecha(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetVentasPorFechaUseCase(client)

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
                data={"daily_sales": []},
            )

        return ApiResponse(
            success=True,
            message="Ventas por fecha obtenidas correctamente",
            data={"daily_sales": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener ventas por fecha. Intente nuevamente.",
            data={"daily_sales": []},
        )


@router.get("/productos-mas-vendidos")
async def get_productos_mas_vendidos(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetProductosMasVendidosUseCase(client)

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
            message="Productos más vendidos obtenidos correctamente",
            data={"products": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener productos más vendidos. Intente nuevamente.",
            data={"products": []},
        )


@router.get("/metodos-pago-mas-usados")
async def get_metodos_pago_mas_usados(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetMetodosPagoMasUsadosUseCase(client)

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
            message="Métodos de pago más usados obtenidos correctamente",
            data={"payment_methods": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener métodos de pago más usados. Intente nuevamente.",
            data={"payment_methods": []},
        )


"""
@router.get("/metodos-pago")
async def get_metodos_pago(
    city: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
    date_from: Optional[date] = None,
    date_until: Optional[date] = None,
):
    try:
        client = await get_starrocks_client()
        use_case = GetMetodosPagoUseCase(client)

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
            message="Métodos de pago obtenidos correctamente",
            data={"payment_methods": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener métodos de pago. Intente nuevamente.",
            data={"payment_methods": []},
        )
"""

@router.get("/categorias")
async def get_categorias():
    try:
        client = await get_starrocks_client()
        use_case = GetCategoriasUseCase(client)
        result = await use_case.execute()

        if not result:
            return ApiResponse(
                success=True,
                message="No hay categorías registradas",
                data={"categories": []},
            )

        return ApiResponse(
            success=True,
            message="Categorías obtenidas correctamente",
            data={"categories": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener categorías. Intente nuevamente.",
            data={"categories": []},
        )


@router.get("/ciudades")
async def get_ciudades():
    try:
        client = await get_starrocks_client()
        use_case = GetCiudadesUseCase(client)
        result = await use_case.execute()

        if not result:
            return ApiResponse(
                success=True,
                message="No hay ciudades registradas",
                data={"cities": []},
            )

        return ApiResponse(
            success=True,
            message="Ciudades obtenidas correctamente",
            data={"cities": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener ciudades. Intente nuevamente.",
            data={"cities": []},
        )


@router.get("/metodos-pago")
async def get_metodos_pago():
    try:
        client = await get_starrocks_client()
        use_case = GetMetodosPagoListUseCase(client)
        result = await use_case.execute()

        if not result:
            return ApiResponse(
                success=True,
                message="No hay métodos de pago registrados",
                data={"payment_methods": []},
            )

        return ApiResponse(
            success=True,
            message="Métodos de pago obtenidos correctamente",
            data={"payment_methods": result},
        )
    except Exception:
        return ApiResponse(
            success=False,
            message="Error al obtener métodos de pago. Intente nuevamente.",
            data={"payment_methods": []},
        )


ALLOWED_CSV_EXTENSIONS = {"csv"}
MAX_FILE_SIZE = 500 * 1024 * 1024

@router.post("/import-csv")
async def import_csv(
    file: UploadFile = File(...),
    delete_existing: bool = Form(False),
):
    if not file.filename or "." not in file.filename:
        raise HTTPException(status_code=400, detail="Archivo inválido: sin extensión")

    ext = file.filename.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED_CSV_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Solo se permiten archivos CSV")

    csv_bytes = await file.read()
    if len(csv_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, detail="El archivo excede el tamaño máximo permitido (16MB)"
        )

    try:
        client = await get_starrocks_client()
        use_case = ImportCsvUseCase(client)
        result = await use_case.execute(csv_bytes, delete_existing=delete_existing)

        return ApiResponse(
            success=True,
            message=f"Se importaron {result['imported']} registros correctamente"
                    + (f" ({result['errors']} errores)" if result['errors'] else ""),
            data=result,
        )
    except ImportCsvError as e:
        return ApiResponse(
            success=False,
            message=e.message,
            data={"imported": 0, "errors": 0},
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            message=f"Error al importar CSV: {str(e)}",
            data={"imported": 0, "errors": 0},
        )
