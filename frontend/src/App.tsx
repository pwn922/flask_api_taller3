import { useState, useCallback } from 'react'
import { useFilters } from './hooks/useFilters'
import { useDashboardData } from './hooks/useDashboardData'
import DashboardLayout from './components/Layout/DashboardLayout'
import FilterBar from './components/Filters/FilterBar'
import TotalVentas from './components/KPIs/TotalVentas'
import PromedioGasto from './components/KPIs/PromedioGasto'
import TopCategory from './components/KPIs/TopCategory'
import TopProduct from './components/KPIs/TopProduct'
import TopCity from './components/KPIs/TopCity'
import TopPaymentMethod from './components/KPIs/TopPaymentMethod'
import VentasPorCategoria from './components/Charts/VentasPorCategoria'
import ComprasPorCiudad from './components/Charts/ComprasPorCiudad'
import ComprasPorRangoEtario from './components/Charts/ComprasPorRangoEtario'
import VentasPorFecha from './components/Charts/VentasPorFecha'
import ProductosMasVendidos from './components/Charts/ProductosMasVendidos'
import MetodosPago from './components/Charts/MetodosPago'
import LoadingSkeleton from './components/Layout/LoadingSkeleton'
import ErrorState from './components/Layout/ErrorState'

function App() {
  const { filters, setFilter, resetFilters } = useFilters()
  const [refreshKey, setRefreshKey] = useState(0)
  const { data, loading, error } = useDashboardData(filters, refreshKey)

  const handleImportDone = useCallback(() => {
    setRefreshKey((k) => k + 1)
  }, [])

  return (
    <DashboardLayout onImportDone={handleImportDone}>
      <div className="space-y-6">
        <FilterBar
          filters={filters}
          onFilterChange={setFilter}
          onReset={resetFilters}
        />

        {loading && <LoadingSkeleton />}

        {error && <ErrorState message={error} onRetry={() => window.location.reload()} />}

        {!loading && !error && (
          <>
            <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
              <TotalVentas total={data.totalVentas} />
              <PromedioGasto promedio={data.promedioGasto} />
              <TopCategory items={data.topCategory} />
              <TopProduct items={data.topProduct} />
              <TopCity items={data.topCity} />
              <TopPaymentMethod items={data.topPaymentMethod} />
            </div>

            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
              <VentasPorCategoria data={data.ventasPorCategoria} />
              <ComprasPorCiudad data={data.comprasPorCiudad} />
              <ComprasPorRangoEtario data={data.comprasPorRangoEtario} />
              <VentasPorFecha data={data.ventasPorFecha} />
              <ProductosMasVendidos data={data.productosMasVendidos} />
              <MetodosPago data={data.metodosPago} />
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  )
}

export default App
