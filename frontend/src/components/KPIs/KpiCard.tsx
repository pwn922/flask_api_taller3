import type { ReactNode } from 'react'

interface KpiCardProps {
  title: string
  value: string
  icon: ReactNode
}

export default function KpiCard({ title, value, icon }: KpiCardProps) {
  return (
    <div className="flex items-center gap-4 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <div className="flex size-12 shrink-0 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
        {icon}
      </div>
      <div className="min-w-0">
        <p className="truncate text-sm font-medium text-gray-500">{title}</p>
        <p className="truncate text-2xl font-bold text-gray-900">{value}</p>
      </div>
    </div>
  )
}
