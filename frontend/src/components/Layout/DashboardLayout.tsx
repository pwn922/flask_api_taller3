import type { ReactNode } from 'react'
import ImportCsvButton from './ImportCsvButton'

interface Props {
  children: ReactNode
  onImportDone?: () => void
}

export default function DashboardLayout({ children, onImportDone }: Props) {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded-lg bg-indigo-600 text-white text-sm font-bold">
              A
            </div>
            <h1 className="text-lg font-bold text-gray-900">Analítica de Compras</h1>
          </div>
          <ImportCsvButton onImportDone={onImportDone} />
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  )
}
