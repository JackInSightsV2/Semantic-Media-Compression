import type {
  FileUploadResponse,
  DistillResponse,
  InflateResponse,
  DistillAndInflateResponse,
  CompareResponse,
  RunListResponse,
  RunDetailsResponse
} from '../types';

const API_BASE = '/api';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
}

export const api = {
  // File upload
  async uploadFile(file: File): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_BASE}/files/upload`, {
      method: 'POST',
      body: formData
    });
    return handleResponse<FileUploadResponse>(response);
  },

  // Distillation
  async distill(file: File | null, filePath: string | null, fileId: string | null, category: string | null, testMode: boolean, maxPasses: number | null): Promise<DistillResponse> {
    const formData = new FormData();
    if (file) formData.append('file', file);
    if (filePath) formData.append('file_path', filePath);
    if (fileId) formData.append('file_id', fileId);
    if (category) formData.append('category', category);
    formData.append('test_mode', testMode.toString());
    if (maxPasses) formData.append('max_passes', maxPasses.toString());

    const response = await fetch(`${API_BASE}/distill`, {
      method: 'POST',
      body: formData
    });
    return handleResponse<DistillResponse>(response);
  },

  // Reinflation
  async inflate(file: File): Promise<InflateResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_BASE}/inflate`, {
      method: 'POST',
      body: formData
    });
    return handleResponse<InflateResponse>(response);
  },

  // Distill and Inflate
  async distillAndInflate(file: File | null, filePath: string | null, fileId: string | null, category: string | null, testMode: boolean, maxPasses: number | null): Promise<DistillAndInflateResponse> {
    const formData = new FormData();
    if (file) formData.append('file', file);
    if (filePath) formData.append('file_path', filePath);
    if (fileId) formData.append('file_id', fileId);
    if (category) formData.append('category', category);
    formData.append('test_mode', testMode.toString());
    if (maxPasses) formData.append('max_passes', maxPasses.toString());

    const response = await fetch(`${API_BASE}/distill-and-inflate`, {
      method: 'POST',
      body: formData
    });
    return handleResponse<DistillAndInflateResponse>(response);
  },

  // Comparison
  async compare(runId: string | null, jsonFile: File | null, inflatedFile: File | null, originalFile: File | null, jsonFilePath: string | null, inflatedFilePath: string | null): Promise<CompareResponse> {
    const formData = new FormData();
    if (runId) formData.append('run_id', runId);
    if (jsonFile) formData.append('json_file', jsonFile);
    if (inflatedFile) formData.append('inflated_file', inflatedFile);
    if (originalFile) formData.append('original_file', originalFile);
    if (jsonFilePath) formData.append('json_file_path', jsonFilePath);
    if (inflatedFilePath) formData.append('inflated_file_path', inflatedFilePath);

    const response = await fetch(`${API_BASE}/compare`, {
      method: 'POST',
      body: formData
    });
    return handleResponse<CompareResponse>(response);
  },

  // Runs
  async listRuns(page: number = 1, limit: number = 50, runType?: string, status?: string): Promise<RunListResponse> {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString()
    });
    if (runType) params.append('run_type', runType);
    if (status) params.append('status', status);

    const response = await fetch(`${API_BASE}/runs?${params}`);
    return handleResponse<RunListResponse>(response);
  },

  async getRunDetails(runId: string): Promise<RunDetailsResponse> {
    const response = await fetch(`${API_BASE}/runs/${runId}`);
    return handleResponse<RunDetailsResponse>(response);
  },

  async getRunFiles(runId: string): Promise<{ run_id: string; file_paths: Record<string, string> }> {
    const response = await fetch(`${API_BASE}/runs/${runId}/files`);
    return handleResponse(response);
  },

  downloadRunFile(runId: string, fileType: string): string {
    return `${API_BASE}/runs/${runId}/download/${fileType}`;
  },

  // Cleanup
  async cleanup(categories: string[]): Promise<{ status: string; cleared_categories: string[]; results: any }> {
    const response = await fetch(`${API_BASE}/cleanup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ categories })
    });
    return handleResponse(response);
  }
};

