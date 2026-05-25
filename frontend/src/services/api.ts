import type {
  ApiResponse,
  TotalVentasData,
  PromedioGastoData,
  CategoryItem,
  ProductItem,
  CityItem,
  PaymentMethodItem,
  DailySale,
  AgeRangeItem,
  Filters,
} from '../types/dashboard'

const BASE_URL = '/api/sales'

function buildQuery(filters: Filters): string {
  const params = new URLSearchParams()
  if (filters.city) params.set('city', filters.city)
  if (filters.category) params.set('category', filters.category)
  if (filters.dateFrom) params.set('date_from', filters.dateFrom)
  if (filters.dateUntil) params.set('date_until', filters.dateUntil)
  if (filters.paymentMethod) params.set('payment_method', filters.paymentMethod)
  const qs = params.toString()
  return qs ? `?${qs}` : ''
}

async function fetchData<T>(endpoint: string, filters: Filters): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}${buildQuery(filters)}`)
  if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`)
  const json: ApiResponse<T> = await res.json()
  if (!json.success) throw new Error(json.message)
  return json.data
}

export async function getTotalVentas(filters: Filters) {
  return fetchData<TotalVentasData>('/total-ventas', filters)
}

export async function getPromedioGasto(filters: Filters) {
  return fetchData<PromedioGastoData>('/promedio-gasto', filters)
}

export async function getTopCategory(filters: Filters) {
  return fetchData<{ categories: CategoryItem[] }>('/top-category', filters)
}

export async function getProductoMasVendido(filters: Filters) {
  return fetchData<{ products: ProductItem[] }>('/producto-mas-vendido', filters)
}

export async function getCiudadMasComprada(filters: Filters) {
  return fetchData<{ cities: CityItem[] }>('/ciudad-mas-comprada', filters)
}

export async function getMetodoPagoMasUsado(filters: Filters) {
  return fetchData<{ payment_methods: PaymentMethodItem[] }>('/metodo-pago-mas-usado', filters)
}

export async function getVentasPorCategoria(filters: Filters) {
  return fetchData<{ categories: CategoryItem[] }>('/ventas-por-categoria', filters)
}

export async function getComprasPorCiudad(filters: Filters) {
  return fetchData<{ cities: CityItem[] }>('/compras-por-ciudad', filters)
}

export async function getComprasPorRangoEtario(filters: Filters) {
  return fetchData<{ age_ranges: AgeRangeItem[] }>('/compras-por-rango-etario', filters)
}

export async function getVentasPorFecha(filters: Filters) {
  return fetchData<{ daily_sales: DailySale[] }>('/ventas-por-fecha', filters)
}

export async function getProductosMasVendidos(filters: Filters, limit = 10) {
  const params = buildQuery(filters)
  const separator = params ? '&' : '?'
  const res = await fetch(`${BASE_URL}/productos-mas-vendidos${params}${separator}limit=${limit}`)
  if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`)
  const json: ApiResponse<{ products: ProductItem[] }> = await res.json()
  if (!json.success) throw new Error(json.message)
  return json.data
}

export async function getMetodosPago(filters: Filters) {
  return fetchData<{ payment_methods: PaymentMethodItem[] }>('/metodos-pago', filters)
}

export interface ImportResult {
  imported: number
  errors: number
  total_lines: number
}

export async function importCsv(file: File, deleteExisting: boolean): Promise<ImportResult> {
  const formData = new FormData()
  formData.set('file', file)
  formData.set('delete_existing', String(deleteExisting))

  const res = await fetch(`${BASE_URL}/import-csv`, {
    method: 'POST',
    body: formData,
  })

  if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`)
  const json: ApiResponse<ImportResult> = await res.json()
  if (!json.success) throw new Error(json.message)
  return json.data
}
