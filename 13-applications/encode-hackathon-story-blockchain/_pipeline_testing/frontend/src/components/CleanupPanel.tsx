import React, { useState } from 'react';
import { api } from '../services/api';

export const CleanupPanel: React.FC = () => {
  const [categories, setCategories] = useState<Record<string, boolean>>({
    documents: false,
    runs: false,
    responses: false,
    outputs: false,
    inflations: false
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [confirmed, setConfirmed] = useState(false);

  const handleCategoryChange = (category: string) => {
    setCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
    setConfirmed(false); // Reset confirmation when categories change
  };

  const handleCleanup = async () => {
    const selectedCategories = Object.entries(categories)
      .filter(([_, selected]) => selected)
      .map(([category, _]) => category);

    if (selectedCategories.length === 0) {
      setError('Please select at least one category to clear');
      return;
    }

    if (!confirmed) {
      setError('Please confirm the cleanup operation');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await api.cleanup(selectedCategories);
      setResult(data);
      // Reset checkboxes after successful cleanup
      setCategories({
        documents: false,
        runs: false,
        responses: false,
        outputs: false,
        inflations: false
      });
      setConfirmed(false);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const selectedCount = Object.values(categories).filter(Boolean).length;

  return (
    <div className="panel">
      <h2>Cleanup Data</h2>
      <p style={{ color: '#666', marginBottom: '20px' }}>
        Select the categories you want to clear. This action cannot be undone.
      </p>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={categories.documents}
            onChange={() => handleCategoryChange('documents')}
          />
          Documents (data/ subdirectories)
        </label>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={categories.runs}
            onChange={() => handleCategoryChange('runs')}
          />
          Runs (run metadata files)
        </label>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={categories.responses}
            onChange={() => handleCategoryChange('responses')}
          />
          Responses (LLM response files)
        </label>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={categories.outputs}
            onChange={() => handleCategoryChange('outputs')}
          />
          Outputs (distillation output files)
        </label>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={categories.inflations}
            onChange={() => handleCategoryChange('inflations')}
          />
          Inflations (reinflation output files)
        </label>
      </div>

      {selectedCount > 0 && (
        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={confirmed}
              onChange={(e) => setConfirmed(e.target.checked)}
            />
            <strong>I confirm I want to delete {selectedCount} categor{selectedCount === 1 ? 'y' : 'ies'}</strong>
          </label>
        </div>
      )}

      <button
        onClick={handleCleanup}
        disabled={loading || selectedCount === 0 || !confirmed}
        style={{
          backgroundColor: selectedCount > 0 && confirmed ? '#e74c3c' : undefined,
          marginTop: '10px'
        }}
      >
        {loading ? 'Cleaning up...' : 'Clear Selected Categories'}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <h3>Cleanup Results:</h3>
          <p><strong>Status:</strong> {result.status}</p>
          <p><strong>Cleared Categories:</strong> {result.cleared_categories.join(', ')}</p>
          <details>
            <summary>Details</summary>
            <pre>{JSON.stringify(result.results, null, 2)}</pre>
          </details>
        </div>
      )}
    </div>
  );
};

