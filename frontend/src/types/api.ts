/**
 * Common API response types
 */

export interface APIResponse<T> {
  data: T;
  message: string;
  errors: APIError[] | null;
  meta?: {
    timestamp: string;
    request_id: string;
  };
}

export interface APIError {
  field: string;
  message: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}
