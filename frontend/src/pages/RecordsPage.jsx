import { useCallback, useEffect, useState } from 'react'
import { RefreshCw } from 'lucide-react'
import SectionHeader from '../components/SectionHeader'
import DataTable from '../components/DataTable'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'
import { getApiError } from '../services/api'
import { extractRows } from '../utils/format'

export default function RecordsPage({ title, description, loader, eyebrow }) {
  const [payload, setPayload] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  // Re-create the loader whenever the route supplies a different API function.
  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    setPayload(null) // Never leave the previous page's rows visible while loading.

    try {
      const result = await loader(100)
      setPayload(result)
    } catch (e) {
      setError(getApiError(e))
    } finally {
      setLoading(false)
    }
  }, [loader])

  // RecordsPage is reused by React Router across routes, so the loader must be
  // a dependency. An empty dependency array would keep the first route's data.
  useEffect(() => {
    let active = true
    setLoading(true)
    setError('')
    setPayload(null)

    const fetchRows = async () => {
      try {
        const result = await loader(100)
        if (active) setPayload(result)
      } catch (e) {
        if (active) setError(getApiError(e))
      } finally {
        if (active) setLoading(false)
      }
    }

    fetchRows()
    return () => { active = false }
  }, [loader])

  const rows = extractRows(payload)

  return <>
    <SectionHeader
      title={title}
      eyebrow={eyebrow}
      description={description}
      action={
        <button
          onClick={load}
          disabled={loading}
          className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
        >
          <RefreshCw size={15} /> Refresh
        </button>
      }
    />

    <div className="overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-soft">
      <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
        <div>
          <h2 className="font-semibold text-ink">Latest records</h2>
          <p className="mt-1 text-xs text-slate-400">Showing up to 100 records from the backend</p>
        </div>
        {!loading && !error && (
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
            {rows.length} rows
          </span>
        )}
      </div>

      {loading ? <LoadingState /> : error ? (
        <div className="p-5"><ErrorState message={error} onRetry={load} /></div>
      ) : <DataTable rows={rows} />}
    </div>
  </>
}
