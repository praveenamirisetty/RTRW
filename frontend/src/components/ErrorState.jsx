import { AlertTriangle } from 'lucide-react'
export default function ErrorState({ message, onRetry }) {
  return (
    <div className="rounded-2xl border border-rose-100 bg-rose-50 p-5 text-sm text-rose-700">
      <div className="flex items-center gap-2 font-semibold"><AlertTriangle size={17} /> Could not load data</div>
      <p className="mt-2 break-words">{message}</p>
      {onRetry && <button onClick={onRetry} className="mt-3 rounded-lg bg-rose-600 px-3 py-2 text-xs font-semibold text-white hover:bg-rose-700">Try again</button>}
    </div>
  )
}
