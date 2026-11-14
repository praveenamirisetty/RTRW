import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api',
  timeout: 30000,
  headers: { Accept: 'application/json' }
})

export const getHealth = async () => (await api.get('/health')).data
export const getOverview = async () => (await api.get('/dashboard/overview')).data
export const getTables = async () => (await api.get('/metadata/tables')).data
export const getTableRows = async (key, limit = 100) =>
  (await api.get(`/metadata/tables/${encodeURIComponent(key)}`, { params: { limit } })).data
export const getRefunds = async (limit = 100) => (await api.get('/refunds', { params: { limit } })).data
export const getExceptions = async (limit = 100) => (await api.get('/exceptions', { params: { limit } })).data
export const getReconciliationRuns = async (limit = 100) =>
  (await api.get('/reconciliation/runs', { params: { limit } })).data
export const getSnapshots = async (limit = 100) =>
  (await api.get('/reconciliation/snapshots', { params: { limit } })).data
export const getIngestionValidation = async (limit = 100) =>
  (await api.get('/ingestion/validation', { params: { limit } })).data

export function getApiError(error) {
  return error?.response?.data?.message || error?.message || 'Unable to connect to the backend.'
}

export default api

// Uses the metadata table endpoint because the dashboard-specific data-quality endpoint
// currently returns an INTERNAL_ERROR in the backend.
export const getDataQualityRows = async (limit = 100) =>
  (await api.get('/metadata/tables/DATA_QUALITY_RESULTS', { params: { limit } })).data
