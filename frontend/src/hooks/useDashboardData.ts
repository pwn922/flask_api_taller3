import { useState, useEffect } from 'react'
import type { Filters, DashboardData } from '../types/dashboard'
import {
  getTotalVentas,
  getPromedioGasto,
  getTopCategory,
  getProductoMasVendido,
  getCiudadMasComprada,
  getMetodoPagoMasUsado,
  getVentasPorCategoria,
  getComprasPorCiudad,
  getComprasPorRangoEtario,
  getVentasPorFecha,
  getProductosMasVendidos,
  getMetodosPago,
} from '../services/api'

const EMPTY: DashboardData = {
  totalVentas: 0,
  promedioGasto: 0,
  topCategory: [],
  topProduct: [],
  topCity: [],
  topPaymentMethod: [],
  ventasPorCategoria: [],
  comprasPorCiudad: [],
  comprasPorRangoEtario: [],
  ventasPorFecha: [],
  productosMasVendidos: [],
  metodosPago: [],
}

export function useDashboardData(filters: Filters, refreshKey?: number) {
  const [data, setData] = useState<DashboardData>(EMPTY)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      setLoading(true)
      setError(null)

      try {
        const [
          totalVentas,
          promedioGasto,
          topCat,
          topProd,
          topCity,
          topPay,
          ventasCat,
          comprasCiu,
          comprasEdad,
          ventasFecha,
          productosTop,
          metodosPago,
        ] = await Promise.all([
          getTotalVentas(filters),
          getPromedioGasto(filters),
          getTopCategory(filters),
          getProductoMasVendido(filters),
          getCiudadMasComprada(filters),
          getMetodoPagoMasUsado(filters),
          getVentasPorCategoria(filters),
          getComprasPorCiudad(filters),
          getComprasPorRangoEtario(filters),
          getVentasPorFecha(filters),
          getProductosMasVendidos(filters),
          getMetodosPago(filters),
        ])

        if (!cancelled) {
          setData({
            totalVentas: totalVentas.total_ventas,
            promedioGasto: promedioGasto.promedio_gasto,
            topCategory: topCat.categories,
            topProduct: topProd.products,
            topCity: topCity.cities,
            topPaymentMethod: topPay.payment_methods,
            ventasPorCategoria: ventasCat.categories,
            comprasPorCiudad: comprasCiu.cities,
            comprasPorRangoEtario: comprasEdad.age_ranges,
            ventasPorFecha: ventasFecha.daily_sales,
            productosMasVendidos: productosTop.products,
            metodosPago: metodosPago.payment_methods,
          })
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : 'Error al cargar datos')
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    load()
    return () => { cancelled = true }
  }, [filters, refreshKey])

  return { data, loading, error }
}
