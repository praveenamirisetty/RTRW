export default function LoadingState({ label = 'Loading data...' }) {
  return <div className="rounded-2xl border border-slate-100 bg-white p-8 text-center text-sm text-slate-500 shadow-soft">{label}</div>
}
