import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from './layouts/AppLayout'
import Dashboard from './pages/Dashboard'
import RecordsPage from './pages/RecordsPage'
import Metadata from './pages/Metadata'
import { getRefunds, getExceptions, getReconciliationRuns, getSnapshots, getIngestionValidation, getDataQualityRows } from './services/api'

export default function App() {
  return <Routes>
    <Route element={<AppLayout/>}>
      <Route index element={<Dashboard/>}/>
      <Route path="reconciliation" element={<RecordsPage title="Reconciliation Runs" description="Recent reconciliation execution records." loader={getReconciliationRuns}/>}/>
      <Route path="snapshots" element={<RecordsPage title="Reconciliation Snapshots" description="Saved reconciliation snapshots from the warehouse." loader={getSnapshots}/>}/>
      <Route path="exceptions" element={<RecordsPage title="Exception Management" description="Exception status-change history returned by the warehouse." loader={getExceptions}/>}/>
      <Route path="refunds" element={<RecordsPage title="Refund Records" description="Refund records available in the RTRW warehouse." loader={getRefunds}/>}/>
      <Route path="data-quality" element={<RecordsPage title="Data Quality" description="Data quality validation results." loader={getDataQualityRows}/>}/>
      <Route path="ingestion" element={<RecordsPage title="S3 Ingestion Validation" description="Latest S3 ingestion validation records." loader={getIngestionValidation}/>}/>
      <Route path="metadata" element={<Metadata/>}/>
      <Route path="*" element={<Navigate to="/" replace/>}/>
    </Route>
  </Routes>
}
