import React, { useState } from 'react';
import { api } from '../services/api';

export const DistillPanel: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [filePath, setFilePath] = useState('');
  const [fileId, setFileId] = useState('');
  const [category, setCategory] = useState('');
  const [testMode, setTestMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!file && !filePath && !fileId) {
      setError('Please provide a file, file path, or file ID');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await api.distill(file, filePath || null, fileId || null, category || null, testMode, null);
      setResult(response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Distill File</h2>
      <div className="form-group">
        <label>Upload File:</label>
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      </div>
      <div className="form-group">
        <label>Or File Path:</label>
        <input type="text" value={filePath} onChange={(e) => setFilePath(e.target.value)} placeholder="data/research_papers/paper.pdf" />
      </div>
      <div className="form-group">
        <label>Or File ID (from upload):</label>
        <input type="text" value={fileId} onChange={(e) => setFileId(e.target.value)} placeholder="UUID" />
      </div>
      <div className="form-group">
        <label>Category (optional):</label>
        <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} placeholder="research, business, fiction, etc." />
      </div>
      <div className="form-group">
        <label>
          <input type="checkbox" checked={testMode} onChange={(e) => setTestMode(e.target.checked)} />
          Test Mode (Pass 1 only)
        </label>
      </div>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Distilling...' : 'Distill'}
      </button>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          <h3>Result:</h3>
          <p><strong>Run ID:</strong> {result.run_id}</p>
          <p><strong>Status:</strong> {result.status}</p>
          <p><strong>Total Tokens:</strong> {result.metrics.total_tokens}</p>
          <p><strong>Total Cost:</strong> ${result.metrics.total_cost.toFixed(4)}</p>
          <details>
            <summary>Blueprint JSON</summary>
            <pre>{JSON.stringify(result.blueprint, null, 2)}</pre>
          </details>
        </div>
      )}
    </div>
  );
};

