import type { Filters } from '../../types/dashboard'

interface Props {
  filters: Filters
  onFilterChange: (key: keyof Filters, value: string | undefined) => void
  onReset: () => void
}

export default function FilterBar({ filters, onFilterChange, onReset }: Props) {
  return (
    <div className="flex flex-wrap items-end gap-4 rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
      <div className="min-w-32">
        <label className="mb-1 block text-xs font-medium text-gray-500">Ciudad</label>
        <input
          type="text"
          placeholder="Todas"
          value={filters.city ?? ''}
          onChange={(e) => onFilterChange('city', e.target.value || undefined)}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        />
      </div>

      <div className="min-w-32">
        <label className="mb-1 block text-xs font-medium text-gray-500">Categoría</label>
        <input
          type="text"
          placeholder="Todas"
          value={filters.category ?? ''}
          onChange={(e) => onFilterChange('category', e.target.value || undefined)}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        />
      </div>

      <div className="min-w-32">
        <label className="mb-1 block text-xs font-medium text-gray-500">Fecha desde</label>
        <input
          type="date"
          value={filters.dateFrom ?? ''}
          onChange={(e) => onFilterChange('dateFrom', e.target.value || undefined)}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        />
      </div>

      <div className="min-w-32">
        <label className="mb-1 block text-xs font-medium text-gray-500">Fecha hasta</label>
        <input
          type="date"
          value={filters.dateUntil ?? ''}
          onChange={(e) => onFilterChange('dateUntil', e.target.value || undefined)}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        />
      </div>

      <div className="min-w-32">
        <label className="mb-1 block text-xs font-medium text-gray-500">Método de pago</label>
        <input
          type="text"
          placeholder="Todos"
          value={filters.paymentMethod ?? ''}
          onChange={(e) => onFilterChange('paymentMethod', e.target.value || undefined)}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        />
      </div>

      <button
        onClick={onReset}
        className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-50"
      >
        Limpiar
      </button>
    </div>
  )
}
