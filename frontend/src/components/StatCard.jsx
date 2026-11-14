import { ArrowUpRight, Database } from 'lucide-react'
import { formatNumber } from '../utils/format'

export default function StatCard({ title, value, hint, icon: Icon = Database, tone = 'blue' }) {
  const tones = {
    blue: 'bg-blue-50 text-blue-600',
    violet: 'bg-violet-50 text-violet-600',
    green: 'bg-emerald-50 text-emerald-600',
    amber: 'bg-amber-50 text-amber-600'
  }
  return (
    <div className="rounded-2xl border border-slate-100 bg-white p-5 shadow-soft">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="mt-3 text-3xl font-bold tracking-tight text-ink">{formatNumber(value)}</p>
        </div>
        <div className={`rounded-xl p-3 ${tones[tone]}`}><Icon size={21} /></div>
      </div>
      <div className="mt-4 flex items-center gap-1 text-xs text-slate-400">
        <ArrowUpRight size={14} /> {hint || 'Live value from Snowflake'}
      </div>
    </div>
  )
}
