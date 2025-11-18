import React, { useState } from 'react';
import { api } from '../services/api';

export const ComparePanel: React.FC = () => {
  const [runId, setRunId] = useState('');
  const [jsonFile, setJsonFile] = useState<File | null>(null);
  const [inflatedFile, setInflatedFile] = useState<File | null>(null);
  const [originalFile, setOriginalFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!runId && (!jsonFile || !inflatedFile)) {
      setError('Please provide run_id or both JSON and inflated files');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await api.compare(runId || null, jsonFile, inflatedFile, originalFile, null, null);
      setResult(response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Compare Files</h2>
      <div className="form-group">
        <label>Run ID (optional):</label>
        <input type="text" value={runId} onChange={(e) => setRunId(e.target.value)} placeholder="UUID" />
      </div>
      <div className="form-group">
        <label>Or JSON File:</label>
        <input type="file" accept=".json" onChange={(e) => setJsonFile(e.target.files?.[0] || null)} />
      </div>
      <div className="form-group">
        <label>And Inflated File:</label>
        <input type="file" accept=".md,.txt" onChange={(e) => setInflatedFile(e.target.files?.[0] || null)} />
      </div>
      <div className="form-group">
        <label>Original File (optional, for better comparison):</label>
        <input type="file" accept=".pdf,.txt,.docx,.epub" onChange={(e) => setOriginalFile(e.target.files?.[0] || null)} />
        <small style={{ display: 'block', marginTop: '0.25rem', color: '#666' }}>
          If not provided, system will try to find it from blueprint metadata
        </small>
      </div>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Comparing...' : 'Compare'}
      </button>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          <h3>Comparison Result:</h3>
          <p><strong>Run ID:</strong> {result.run_id}</p>
          <p><strong>Status:</strong> {result.status}</p>
          
          {/* Download button */}
          {result.report_path && (
            <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
              <a
                href={api.downloadRunFile(result.run_id, 'comparison_report')}
                download
                className="button"
                style={{ textDecoration: 'none', display: 'inline-block' }}
              >
                Download Comparison Report JSON
              </a>
            </div>
          )}
          
          <div className="scores">
            <h4>Similarity Scores:</h4>
            <ul>
              <li>Semantic Similarity: {result.similarity_scores.semantic_similarity}%</li>
              <li>Structure Preservation: {result.similarity_scores.structure_preservation}%</li>
              <li>Layout Fidelity: {result.similarity_scores.layout_fidelity}%</li>
              <li>Information Completeness: {result.similarity_scores.information_completeness}%</li>
              <li>Overall Fidelity: {result.similarity_scores.overall_fidelity}%</li>
            </ul>
          </div>
          
          {result.similarity_scores.strengths && result.similarity_scores.strengths.length > 0 && (
            <details>
              <summary>Strengths</summary>
              <ul>
                {result.similarity_scores.strengths.map((strength: string, index: number) => (
                  <li key={index}>{strength}</li>
                ))}
              </ul>
            </details>
          )}
          
          {result.similarity_scores.weaknesses && result.similarity_scores.weaknesses.length > 0 && (
            <details>
              <summary>Weaknesses</summary>
              <ul>
                {result.similarity_scores.weaknesses.map((weakness: string, index: number) => (
                  <li key={index}>{weakness}</li>
                ))}
              </ul>
            </details>
          )}
          
          {result.similarity_scores.detailed_analysis && (
            <details>
              <summary>Detailed Analysis</summary>
              <p style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{result.similarity_scores.detailed_analysis}</p>
            </details>
          )}
          
          {result.metrics && (
            <details>
              <summary>Metrics</summary>
              <pre>{JSON.stringify(result.metrics, null, 2)}</pre>
            </details>
          )}
        </div>
      )}
    </div>
  );
};

