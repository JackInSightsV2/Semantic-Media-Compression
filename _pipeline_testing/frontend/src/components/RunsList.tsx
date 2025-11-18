import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { RunListItem } from '../types';

export const RunsList: React.FC = () => {
  const [runs, setRuns] = useState<RunListItem[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [runType, setRunType] = useState<string>('');
  const [status, setStatus] = useState<string>('');

  const loadRuns = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.listRuns(page, 50, runType || undefined, status || undefined);
      setRuns(response.runs);
      setTotal(response.total);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRuns();
  }, [page, runType, status]);

  return (
    <div className="panel">
      <h2>Runs List</h2>
      <div className="filters">
        <select value={runType} onChange={(e) => { setRunType(e.target.value); setPage(1); }}>
          <option value="">All Types</option>
          <option value="distillation">Distillation</option>
          <option value="reinflation">Reinflation</option>
          <option value="comparison">Comparison</option>
          <option value="distill_and_inflate">Distill & Inflate</option>
          <option value="file_upload">File Upload</option>
        </select>
        <select value={status} onChange={(e) => { setStatus(e.target.value); setPage(1); }}>
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="processing">Processing</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
        </select>
        <button onClick={loadRuns}>Refresh</button>
      </div>
      {error && <div className="error">{error}</div>}
      {loading ? (
        <div>Loading...</div>
      ) : (
        <>
          <p>Total: {total} runs</p>
          <table className="runs-table">
            <thead>
              <tr>
                <th>Run ID</th>
                <th>Type</th>
                <th>Status</th>
                <th>Created</th>
                <th>Completed</th>
              </tr>
            </thead>
            <tbody>
              {runs.map((run) => (
                <tr key={run.run_id}>
                  <td><code title={run.run_id}>{run.run_id}</code></td>
                  <td>{run.type}</td>
                  <td>{run.status}</td>
                  <td>{new Date(run.created_at).toLocaleString()}</td>
                  <td>{run.completed_at ? new Date(run.completed_at).toLocaleString() : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="pagination">
            <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>Previous</button>
            <span>Page {page}</span>
            <button onClick={() => setPage(p => p + 1)} disabled={runs.length < 50}>Next</button>
          </div>
        </>
      )}
    </div>
  );
};

