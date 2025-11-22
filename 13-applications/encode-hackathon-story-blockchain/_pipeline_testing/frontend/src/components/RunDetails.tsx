import React, { useState } from 'react';
import { api } from '../services/api';
import type { RunDetailsResponse } from '../types';

export const RunDetails: React.FC = () => {
  const [runId, setRunId] = useState('');
  const [details, setDetails] = useState<RunDetailsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLoad = async () => {
    if (!runId) {
      setError('Please enter a run ID');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await api.getRunDetails(runId);
      setDetails(response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Run Details</h2>
      <div className="form-group">
        <input type="text" value={runId} onChange={(e) => setRunId(e.target.value)} placeholder="Run ID (UUID)" />
        <button onClick={handleLoad} disabled={loading}>
          {loading ? 'Loading...' : 'Load Details'}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
      {details && (
        <div className="result">
          <h3>Run Details:</h3>
          <p><strong>Run ID:</strong> {details.run_id}</p>
          <p><strong>Type:</strong> {details.type}</p>
          <p><strong>Status:</strong> {details.status}</p>
          <p><strong>Created:</strong> {new Date(details.created_at).toLocaleString()}</p>
          {details.completed_at && <p><strong>Completed:</strong> {new Date(details.completed_at).toLocaleString()}</p>}
          {details.error_message && <p className="error"><strong>Error:</strong> {details.error_message}</p>}
          
          {/* Download buttons */}
          {details.file_paths && Object.keys(details.file_paths).length > 0 && (
            <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
              <h4>Downloads:</h4>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {/* For distillation runs, show blueprint download */}
                {details.type === 'distillation' && details.file_paths.blueprint && (
                  <a
                    href={api.downloadRunFile(details.run_id, 'blueprint')}
                    download
                    className="button"
                    style={{ textDecoration: 'none' }}
                  >
                    Download Blueprint JSON
                  </a>
                )}
                {details.file_paths.quality_report && (
                  <a
                    href={api.downloadRunFile(details.run_id, 'quality_report')}
                    download
                    className="button"
                    style={{ textDecoration: 'none' }}
                  >
                    Download Quality Report
                  </a>
                )}
                {details.file_paths.comparison_report && (
                  <a
                    href={api.downloadRunFile(details.run_id, 'comparison_report')}
                    download
                    className="button"
                    style={{ textDecoration: 'none' }}
                  >
                    Download Comparison Report
                  </a>
                )}
                {(details.file_paths.inflated_file || details.file_paths.inflated_md) && (
                  <a
                    href={api.downloadRunFile(details.run_id, details.file_paths.inflated_file ? 'inflated_file' : 'inflated_md')}
                    download
                    className="button"
                    style={{ textDecoration: 'none' }}
                  >
                    Download Inflated File
                  </a>
                )}
                {/* For reinflation runs, show blueprint download if available */}
                {details.type === 'reinflation' && details.file_paths.blueprint && (
                  details.file_paths.blueprint !== 'uploaded' ? (
                    <a
                      href={api.downloadRunFile(details.run_id, 'blueprint')}
                      download
                      className="button"
                      style={{ textDecoration: 'none' }}
                    >
                      Download Blueprint JSON
                    </a>
                  ) : (
                    <span
                      className="button"
                      style={{ 
                        textDecoration: 'none', 
                        opacity: 0.6, 
                        cursor: 'not-allowed',
                        display: 'inline-block'
                      }}
                      title="Blueprint was uploaded but not saved to disk for this run"
                    >
                      Download Blueprint JSON (Not Available)
                    </span>
                  )
                )}
              </div>
            </div>
          )}
          
          <details>
            <summary>File Paths</summary>
            <pre>{JSON.stringify(details.file_paths, null, 2)}</pre>
          </details>
          <details>
            <summary>Metrics</summary>
            <pre>{JSON.stringify(details.metrics, null, 2)}</pre>
          </details>
          <details>
            <summary>Metadata</summary>
            <pre>{JSON.stringify(details.metadata, null, 2)}</pre>
          </details>
          
          {/* Show comparison data if this is a comparison run */}
          {details.type === 'comparison' && details.metadata?.comparison_data && (
            <details>
              <summary>Comparison Details</summary>
              <div style={{ marginTop: '1rem' }}>
                <h4>Similarity Scores:</h4>
                <ul>
                  <li>Semantic Similarity: {details.metadata.comparison_data.semantic_similarity}%</li>
                  <li>Structure Preservation: {details.metadata.comparison_data.structure_preservation}%</li>
                  <li>Layout Fidelity: {details.metadata.comparison_data.layout_fidelity}%</li>
                  <li>Information Completeness: {details.metadata.comparison_data.information_completeness}%</li>
                  <li>Overall Fidelity: {details.metadata.comparison_data.overall_fidelity}%</li>
                </ul>
                
                {details.metadata.comparison_data.strengths && details.metadata.comparison_data.strengths.length > 0 && (
                  <div style={{ marginTop: '1rem' }}>
                    <h4>Strengths:</h4>
                    <ul>
                      {details.metadata.comparison_data.strengths.map((strength: string, index: number) => (
                        <li key={index}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {details.metadata.comparison_data.weaknesses && details.metadata.comparison_data.weaknesses.length > 0 && (
                  <div style={{ marginTop: '1rem' }}>
                    <h4>Weaknesses:</h4>
                    <ul>
                      {details.metadata.comparison_data.weaknesses.map((weakness: string, index: number) => (
                        <li key={index}>{weakness}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {details.metadata.comparison_data.detailed_analysis && (
                  <div style={{ marginTop: '1rem' }}>
                    <h4>Detailed Analysis:</h4>
                    <p style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{details.metadata.comparison_data.detailed_analysis}</p>
                  </div>
                )}
              </div>
            </details>
          )}
        </div>
      )}
    </div>
  );
};

