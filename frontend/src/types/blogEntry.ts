/**
 * Blog entry related types
 */

export interface BlogEntry {
  id: string;
  user_id: string;
  title: string;
  content: string;
  excerpt: string | null;
  slug: string | null;
  status: 'draft' | 'published' | 'archived';
  is_public: boolean;
  is_featured: boolean;
  view_count: number;
  published_at: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface BlogEntryCreate {
  title: string;
  content: string;
  excerpt?: string;
  status?: 'draft' | 'published' | 'archived';
  is_public?: boolean;
  is_featured?: boolean;
}

export interface BlogEntryUpdate {
  title?: string;
  content?: string;
  excerpt?: string;
  status?: 'draft' | 'published' | 'archived';
  is_public?: boolean;
  is_featured?: boolean;
}

export interface PaginatedBlogEntries {
  items: BlogEntry[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}
