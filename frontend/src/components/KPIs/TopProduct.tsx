import KpiCard from './KpiCard'
import type { ProductItem } from '../../types/dashboard'

interface Props {
  items: ProductItem[]
}

function ProductIcon() {
  return (
    <svg className="size-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
    </svg>
  )
}

export default function TopProduct({ items }: Props) {
  const label = items.length > 0 ? items[0].product : 'N/A'
  return <KpiCard title="Producto Top" value={label} icon={<ProductIcon />} />
}
