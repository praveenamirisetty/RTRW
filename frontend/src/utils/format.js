export function formatNumber(value) {
  if (value === null || value === undefined || Number(value) < 0) return '—'
  return new Intl.NumberFormat('en-US').format(Number(value))
}

export function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return '—'
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 }).format(Number(value))
}

export function humanize(value) {
  return String(value ?? '').replaceAll('_', ' ').toLowerCase().replace(/\b\w/g, c => c.toUpperCase())
}

export function extractRows(payload) {
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload?.rows)) return payload.rows
  if (Array.isArray(payload?.data)) return payload.data
  return []
}
