import React, { useState } from 'react';
import { api } from '../services/api';

export const DistillAndInflatePanel: React.FC = () => {
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
      const response = await api.distillAndInflate(file, filePath || null, fileId || null, category || null, testMode, null);
      setResult(response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Distill & Inflate</h2>
      <div className="form-group">
        <label>Upload File:</label>
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      </div>
      <div className="form-group">
        <label>Or File Path:</label>
        <input type="text" value={filePath} onChange={(e) => setFilePath(e.target.value)} placeholder="data/research_papers/paper.pdf" />
      </div>
      <div className="form-group">
        <label>Or File ID:</label>
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
        {loading ? 'Processing...' : 'Distill & Inflate'}
      </button>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          <h3>Result:</h3>
          <p><strong>Run ID:</strong> {result.run_id}</p>
          <p><strong>Status:</strong> {result.status}</p>
          
          {/* Metrics Summary */}
          <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
            <h4>Metrics:</h4>
            <p><strong>Total Tokens:</strong> {result.metrics.total_tokens || (result.metrics.distillation?.total_tokens || 0) + (result.metrics.reinflation?.total_tokens || 0)}</p>
            <p><strong>Total Cost:</strong> ${((result.metrics.total_cost || (result.metrics.distillation?.total_cost || 0) + (result.metrics.reinflation?.total_cost || 0))).toFixed(4)}</p>
            {result.metrics.distillation && (
              <p><strong>Distillation LLM Calls:</strong> {result.metrics.distillation.total_llm_calls || 0}</p>
            )}
            {result.metrics.reinflation && (
              <p><strong>Reinflation LLM Calls:</strong> {result.metrics.reinflation.total_llm_calls || 0}</p>
            )}
            {result.metrics.distillation && result.metrics.distillation.average_response_time_ms && (
              <p><strong>Distillation Avg Response Time:</strong> {result.metrics.distillation.average_response_time_ms.toFixed(2)}ms</p>
            )}
            {result.metrics.reinflation && result.metrics.reinflation.average_response_time_ms && (
              <p><strong>Reinflation Avg Response Time:</strong> {result.metrics.reinflation.average_response_time_ms.toFixed(2)}ms</p>
            )}
          </div>
          
          {/* Download buttons */}
          <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
            <h4>Downloads:</h4>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {result.outputs?.blueprint_path && (
                <a
                  href={api.downloadRunFile(result.run_id, 'blueprint')}
                  download
                  className="button"
                  style={{ textDecoration: 'none', display: 'inline-block' }}
                >
                  Download Blueprint JSON
                </a>
              )}
              {(result.outputs?.inflated_md_path || result.outputs?.inflated_file) && (
                <a
                  href={api.downloadRunFile(result.run_id, result.outputs?.inflated_file ? 'inflated_file' : 'inflated_md')}
                  download
                  className="button"
                  style={{ textDecoration: 'none', display: 'inline-block' }}
                >
                  Download Inflated Markdown
                </a>
              )}
              {result.outputs?.quality_report_path && (
                <a
                  href={api.downloadRunFile(result.run_id, 'quality_report')}
                  download
                  className="button"
                  style={{ textDecoration: 'none', display: 'inline-block' }}
                >
                  Download Quality Report
                </a>
              )}
            </div>
          </div>
          
          <details>
            <summary>Blueprint JSON</summary>
            <pre style={{ maxHeight: '400px', overflow: 'auto' }}>{JSON.stringify(result.blueprint, null, 2)}</pre>
          </details>
          <details>
            <summary>Inflated Markdown</summary>
            <pre style={{ whiteSpace: 'pre-wrap', maxHeight: '400px', overflow: 'auto' }}>{result.inflated_md}</pre>
          </details>
          <details>
            <summary>Full Metrics</summary>
            <pre>{JSON.stringify(result.metrics, null, 2)}</pre>
          </details>
        </div>
      )}
    </div>
  );
};

