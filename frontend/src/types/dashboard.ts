export interface Filters {
  city?: string
  category?: string
  dateFrom?: string
  dateUntil?: string
  paymentMethod?: string
}

export interface ApiResponse<T> {
  success: boolean
  message: string
  data: T
}

export interface TotalVentasData {
  total_ventas: number
}

export interface PromedioGastoData {
  promedio_gasto: number
}

export interface CategoryItem {
  category: string
  total: number
}

export interface ProductItem {
  product: string
  total: number
}

export interface CityItem {
  city: string
  total: number
}

export interface PaymentMethodItem {
  payment_method: string
  total: number
}

export interface DailySale {
  date: string
  total: number
}

export interface AgeRangeItem {
  range: string
  total: number
}

export interface DashboardData {
  totalVentas: number
  promedioGasto: number
  topCategory: CategoryItem[]
  topProduct: ProductItem[]
  topCity: CityItem[]
  topPaymentMethod: PaymentMethodItem[]
  ventasPorCategoria: CategoryItem[]
  comprasPorCiudad: CityItem[]
  comprasPorRangoEtario: AgeRangeItem[]
  ventasPorFecha: DailySale[]
  productosMasVendidos: ProductItem[]
  metodosPago: PaymentMethodItem[]
}
