import { NavLink, Outlet } from 'react-router-dom'
import { Activity, BarChart3, Boxes, ClipboardList, Database, FileCheck2, LayoutDashboard, RefreshCw, Wallet } from 'lucide-react'

const nav = [
  { to: '/', label: 'Executive Overview', icon: LayoutDashboard, end: true },
  { to: '/reconciliation', label: 'Reconciliation Runs', icon: RefreshCw },
  { to: '/snapshots', label: 'Reconciliation Snapshots', icon: ClipboardList },
  { to: '/exceptions', label: 'Exceptions', icon: ClipboardList },
  { to: '/refunds', label: 'Refunds', icon: Wallet },
  { to: '/data-quality', label: 'Data Quality', icon: FileCheck2 },
  { to: '/ingestion', label: 'S3 Ingestion', icon: Boxes },
  { to: '/metadata', label: 'Warehouse Tables', icon: Database }
]

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-[#f6f8fb] lg:flex">
      <aside className="border-b border-slate-200 bg-white lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col lg:border-b-0 lg:border-r">
        <div className="flex items-center gap-3 px-6 py-5">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 text-white"><Activity size={22}/></div>
          <div><p className="text-lg font-extrabold tracking-tight text-ink">RTRW</p><p className="text-[10px] font-semibold uppercase tracking-[0.17em] text-slate-400">Finance workspace</p></div>
        </div>
        <div className="px-4 pb-2 pt-3 text-[10px] font-bold uppercase tracking-[0.16em] text-slate-400">Workspace</div>
        <nav className="flex gap-1 overflow-x-auto px-3 pb-4 lg:flex-col">
          {nav.map(({ to, label, icon: Icon, end }) => <NavLink key={to} to={to} end={end}
            className={({ isActive }) => `flex shrink-0 items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${isActive ? 'bg-brand-50 text-brand-700' : 'text-slate-500 hover:bg-slate-50 hover:text-ink'}`}>
            <Icon size={18}/><span>{label}</span>
          </NavLink>)}
        </nav>
        <div className="mt-auto hidden border-t border-slate-100 p-5 lg:block">
          <div className="rounded-xl bg-slate-50 p-3">
            <p className="text-xs font-semibold text-slate-700">RTRW Data Warehouse</p>
            <p className="mt-1 text-[11px] text-slate-400">Snowflake · Read-only connection</p>
          </div>
        </div>
      </aside>
      <div className="min-w-0 flex-1 lg:pl-64">
        <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-slate-200/80 bg-white/90 px-5 backdrop-blur sm:px-8">
          <div><p className="text-sm font-semibold text-ink">Returns-to-Refund Reconciliation</p><p className="text-xs text-slate-400">Financial operations portal</p></div>
          <div className="flex items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700"><span className="h-2 w-2 rounded-full bg-emerald-500"/> API workspace</div>
        </header>
        <main className="mx-auto max-w-[1500px] p-5 sm:p-8"><Outlet /></main>
      </div>
    </div>
  )
}
