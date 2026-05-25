import KpiCard from './KpiCard'
import type { CategoryItem } from '../../types/dashboard'

interface Props {
  items: CategoryItem[]
}

function CategoryIcon() {
  return (
    <svg className="size-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 6h.008v.008H6V6Z" />
    </svg>
  )
}

export default function TopCategory({ items }: Props) {
  const label = items.length > 0 ? items[0].category : 'N/A'
  return <KpiCard title="Categoría Top" value={label} icon={<CategoryIcon />} />
}
