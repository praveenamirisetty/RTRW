import { humanize } from '../utils/format'

export default function DataTable({ rows = [], empty = 'No records returned.', maxRows = 100 }) {
  const visible = rows.slice(0, maxRows)
  const columns = [...new Set(visible.flatMap(row => Object.keys(row || {})))].slice(0, 12)
  if (!visible.length) return <div className="p-8 text-center text-sm text-slate-400">{empty}</div>
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
          <tr>{columns.map(col => <th key={col} className="whitespace-nowrap px-4 py-3 font-semibold">{humanize(col)}</th>)}</tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {visible.map((row, i) => <tr key={i} className="hover:bg-slate-50/70">
            {columns.map(col => <td key={col} className="max-w-xs whitespace-nowrap px-4 py-3 text-slate-600">{formatCell(row?.[col])}</td>)}
          </tr>)}
        </tbody>
      </table>
    </div>
  )
}

function formatCell(value) {
  if (value === null || value === undefined) return '—'
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}
