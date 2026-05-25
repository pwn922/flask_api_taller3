import KpiCard from './KpiCard'
import type { PaymentMethodItem } from '../../types/dashboard'

interface Props {
  items: PaymentMethodItem[]
}

function PaymentIcon() {
  return (
    <svg className="size-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 0 0 2.25-2.25V6.75A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25v10.5A2.25 2.25 0 0 0 4.5 19.5Z" />
    </svg>
  )
}

export default function TopPaymentMethod({ items }: Props) {
  const label = items.length > 0 ? items[0].payment_method : 'N/A'
  return <KpiCard title="Método de Pago Top" value={label} icon={<PaymentIcon />} />
}
