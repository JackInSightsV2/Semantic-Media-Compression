export interface FileUploadResponse {
  file_id: string;
  category: string;
  file_path: string;
  saved_at: string;
}

export interface DistillResponse {
  run_id: string;
  status: string;
  blueprint: any;
  metrics: {
    total_tokens: number;
    total_cost: number;
    average_response_time_ms: number;
    [key: string]: any;
  };
  outputs: {
    blueprint_path: string;
    quality_report_path: string;
  };
}

export interface InflateResponse {
  run_id: string;
  status: string;
  inflated_md: string;
  metrics: {
    total_tokens: number;
    total_cost: number;
    [key: string]: any;
  };
  outputs: {
    inflated_md_path: string;
  };
}

export interface DistillAndInflateResponse {
  run_id: string;
  status: string;
  blueprint: any;
  inflated_md: string;
  metrics: any;
  outputs: any;
}

export interface CompareResponse {
  run_id: string;
  status: string;
  similarity_scores: {
    semantic_similarity: number;
    structure_preservation: number;
    layout_fidelity: number;
    information_completeness: number;
    overall_fidelity: number;
    [key: string]: any;
  };
  report_path: string;
  metrics: any;
}

export interface RunListItem {
  run_id: string;
  type: string;
  status: string;
  created_at: string;
  completed_at: string | null;
}

export interface RunListResponse {
  runs: RunListItem[];
  total: number;
  page: number;
  limit: number;
}

export interface RunDetailsResponse {
  run_id: string;
  type: string;
  status: string;
  created_at: string;
  completed_at: string | null;
  error_message: string | null;
  file_paths: Record<string, string>;
  metrics: {
    total_tokens: number;
    total_cost: number;
    [key: string]: any;
  };
  metadata: Record<string, any>;
}

