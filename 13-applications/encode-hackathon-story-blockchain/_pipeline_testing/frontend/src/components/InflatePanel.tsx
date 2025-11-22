import React, { useState } from 'react';
import { api } from '../services/api';

export const InflatePanel: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a JSON file');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await api.inflate(file);
      setResult(response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Inflate Blueprint</h2>
      <div className="form-group">
        <input type="file" accept=".json" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button onClick={handleSubmit} disabled={!file || loading}>
          {loading ? 'Inflating...' : 'Inflate'}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          <h3>Result:</h3>
          <p><strong>Run ID:</strong> {result.run_id}</p>
          <p><strong>Status:</strong> {result.status}</p>
          <p><strong>Total Tokens:</strong> {result.metrics.total_tokens}</p>
          <p><strong>Total Cost:</strong> ${result.metrics.total_cost.toFixed(4)}</p>
          <p><strong>LLM Calls:</strong> {result.metrics.total_llm_calls}</p>
          <p><strong>Avg Response Time:</strong> {result.metrics.average_response_time_ms.toFixed(2)}ms</p>
          
          {/* Download button */}
          {result.outputs?.inflated_md_path && (
            <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
              <a
                href={api.downloadRunFile(result.run_id, 'inflated_file')}
                download
                className="button"
                style={{ textDecoration: 'none', display: 'inline-block' }}
              >
                Download Inflated Markdown
              </a>
            </div>
          )}
          
          <details>
            <summary>Inflated Markdown</summary>
            <pre style={{ whiteSpace: 'pre-wrap', maxHeight: '400px', overflow: 'auto' }}>{result.inflated_md}</pre>
          </details>
          
          <details>
            <summary>Metrics</summary>
            <pre>{JSON.stringify(result.metrics, null, 2)}</pre>
          </details>
        </div>
      )}
    </div>
  );
};

