import { useRef, useState } from 'react'
import { importCsv, type ImportResult } from '../../services/api'

export default function ImportCsvButton({ onImportDone }: { onImportDone?: () => void }) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState<ImportResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [deleteExisting, setDeleteExisting] = useState(false)

  const handleFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    setResult(null)
    setError(null)

    try {
      const data = await importCsv(file, deleteExisting)
      setResult(data)
      onImportDone?.()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al importar')
    } finally {
      setUploading(false)
      if (inputRef.current) inputRef.current.value = ''
    }
  }

  return (
    <div className="relative flex flex-col items-end gap-1">
      <input
        ref={inputRef}
        type="file"
        accept=".csv"
        onChange={handleFile}
        className="hidden"
      />

      <button
        onClick={() => inputRef.current?.click()}
        disabled={uploading}
        className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700 disabled:opacity-50"
      >
        {uploading ? (
          <>
            <svg className="size-4 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            Importando...
          </>
        ) : (
          <>
            <svg className="size-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
            </svg>
            Importar CSV
          </>
        )}
      </button>

      <label className="mt-1 flex items-center gap-2 text-xs text-gray-500">
        <input
          type="checkbox"
          checked={deleteExisting}
          onChange={(e) => setDeleteExisting(e.target.checked)}
          className="size-3.5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />
        Reemplazar datos existentes
      </label>

      {(result || error) && (
        <div className="absolute right-0 top-full z-50 mt-2 w-80 rounded-xl border border-gray-200 bg-white p-4 shadow-lg">
          {error && (
            <div className="flex items-start gap-3">
              <svg className="mt-0.5 size-5 shrink-0 text-red-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
              </svg>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}
          {result && (
            <div className="flex items-start gap-3">
              <svg className="mt-0.5 size-5 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
              <div>
                <p className="text-sm font-medium text-green-800">Importación exitosa</p>
                <p className="text-xs text-green-600">
                  {result.imported} registros importados
                  {result.errors > 0 && ` · ${result.errors} errores`}
                  {result.total_lines > 0 && ` · ${result.total_lines} líneas`}
                </p>
              </div>
            </div>
          )}
          <button
            onClick={() => { setResult(null); setError(null) }}
            className="mt-3 w-full rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-600 hover:bg-gray-200"
          >
            Cerrar
          </button>
        </div>
      )}
    </div>
  )
}
