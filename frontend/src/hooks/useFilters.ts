import { useState, useCallback } from 'react'
import type { Filters } from '../types/dashboard'

const INITIAL_FILTERS: Filters = {
  city: undefined,
  category: undefined,
  dateFrom: undefined,
  dateUntil: undefined,
  paymentMethod: undefined,
}

export function useFilters() {
  const [filters, setFilters] = useState<Filters>(INITIAL_FILTERS)

  const setFilter = useCallback((key: keyof Filters, value: string | undefined) => {
    setFilters((prev) => ({ ...prev, [key]: value || undefined }))
  }, [])

  const resetFilters = useCallback(() => {
    setFilters(INITIAL_FILTERS)
  }, [])

  return { filters, setFilter, resetFilters }
}
