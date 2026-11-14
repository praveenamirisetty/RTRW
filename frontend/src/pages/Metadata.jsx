import { useEffect, useState } from 'react'
import SectionHeader from '../components/SectionHeader'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'
import { getTables, getApiError } from '../services/api'

export default function Metadata() {
  const [tables, setTables] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const load = async () => { setLoading(true); setError(''); try { setTables(await getTables()) } catch(e) { setError(getApiError(e)) } finally { setLoading(false) } }
  useEffect(() => { load() }, [])
  return <>
    <SectionHeader title="Warehouse Tables" description="Approved read-only table catalog exposed by the Spring Boot backend."/>
    {loading ? <LoadingState/> : error ? <ErrorState message={error} onRetry={load}/> :
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {tables.map(t => <div key={t.key} className="rounded-2xl border border-slate-100 bg-white p-5 shadow-soft">
          <p className="text-xs font-bold uppercase tracking-wider text-brand-600">{t.schema}</p>
          <h2 className="mt-2 font-semibold text-ink">{t.table}</h2>
          <p className="mt-2 text-sm text-slate-500">{t.description}</p>
          <p className="mt-4 border-t border-slate-100 pt-3 text-xs text-slate-400">Key: {t.key}</p>
        </div>)}
      </div>}
  </>
}
