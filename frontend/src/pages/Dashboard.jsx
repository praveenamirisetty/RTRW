import { useEffect, useState } from 'react'
import { Activity, CreditCard, Package, RotateCcw, ShoppingCart, Store, Users, RefreshCw } from 'lucide-react'
import { getOverview, getApiError } from '../services/api'
import StatCard from '../components/StatCard'
import SectionHeader from '../components/SectionHeader'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

const labels = [
  ['RAW_ORDERS', 'Orders', ShoppingCart, 'blue'],
  ['RAW_PAYMENTS', 'Payments', CreditCard, 'green'],
  ['RAW_ORDER_ITEMS', 'Order Items', Package, 'violet'],
  ['RAW_CUSTOMERS', 'Customers', Users, 'amber'],
  ['RAW_SELLERS', 'Sellers', Store, 'blue'],
  ['RAW_PRODUCTS', 'Products', BoxesIcon, 'violet'],
  ['RAW_REFUNDS', 'Refund Records', RotateCcw, 'amber']
]
function BoxesIcon(props) { return <Activity {...props}/> }

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const load = async () => {
    setLoading(true); setError('')
    try { setData(await getOverview()) } catch (e) { setError(getApiError(e)) } finally { setLoading(false) }
  }
  useEffect(() => { load() }, [])
  const counts = data?.tableCounts || {}
  const total = Object.values(counts).filter(v => Number(v) >= 0).reduce((a, b) => a + Number(b), 0)
  return <>
    <SectionHeader title="Executive Overview" description="A live view of the records currently available in your RTRW Snowflake warehouse."
      action={<button onClick={load} className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50"><RefreshCw size={15}/> Refresh</button>} />
    {loading ? <LoadingState label="Loading warehouse metrics..." /> : error ? <ErrorState message={error} onRetry={load}/> : <>
      <div className="mb-5 rounded-2xl border border-blue-100 bg-blue-50/70 p-4 text-sm text-blue-800">
        <span className="font-semibold">Warehouse records:</span> {new Intl.NumberFormat('en-US').format(total)} across readable catalog tables. These are row counts, not financial totals.
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {labels.map(([key, title, icon, tone]) => <StatCard key={key} title={title} value={counts[key]} icon={icon} tone={tone}/>)}
      </div>
      <div className="mt-6 grid gap-4 xl:grid-cols-2">
        <div className="rounded-2xl border border-slate-100 bg-white p-5 shadow-soft">
          <h2 className="font-semibold text-ink">Reconciliation & audit records</h2>
          <p className="mt-1 text-xs text-slate-400">Counts returned by the backend table catalog</p>
          <div className="mt-4 grid grid-cols-2 gap-3">
            {['RECONCILIATION_RUN','RECONCILIATION_SNAPSHOT','EXCEPTION_HISTORY','DATA_QUALITY_RESULTS','S3_INGESTION_VALIDATION'].map(k =>
              <div key={k} className="rounded-xl bg-slate-50 p-3"><p className="text-xs text-slate-500">{k.replaceAll('_',' ')}</p><p className="mt-1 text-xl font-bold text-ink">{counts[k] ?? '—'}</p></div>)}
          </div>
        </div>
        <div className="rounded-2xl border border-slate-100 bg-white p-5 shadow-soft">
          <h2 className="font-semibold text-ink">Connection overview</h2>
          <div className="mt-4 space-y-3 text-sm">
            <div className="flex justify-between"><span className="text-slate-500">Frontend</span><span className="font-medium text-emerald-700">Running</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Backend API</span><span className="font-medium text-slate-700">localhost:8080</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Data warehouse</span><span className="font-medium text-slate-700">RTRW_DB</span></div>
            <div className="flex justify-between"><span className="text-slate-500">Warehouse</span><span className="font-medium text-slate-700">RTRW_WH</span></div>
          </div>
          <p className="mt-4 rounded-lg bg-amber-50 p-3 text-xs leading-5 text-amber-800">Finance KPIs such as matched value, refund rate and exception aging are not inferred from row counts. They should be connected to verified analytical views/measures.</p>
        </div>
      </div>
    </>}
  </>
}
