import React, { useState } from 'react';
import { api } from '../services/api';

export const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    try {
      const response = await api.uploadFile(file);
      setResult(response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Upload File</h2>
      <div className="form-group">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={!file || loading}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          <h3>Upload Result:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

