/**
 * BlogEntryList component for displaying and managing blog entries
 */

import React from 'react';
import type { BlogEntry } from '../../types/blogEntry';
import Button from '../common/Button';
import './BlogEntryList.css';

interface BlogEntryListProps {
  entries: BlogEntry[];
  onEdit: (entry: BlogEntry) => void;
  onDelete: (entryId: string) => void;
  onView: (entry: BlogEntry) => void;
  onGenerateFromReview?: () => void;
  loading?: boolean;
}

const BlogEntryList: React.FC<BlogEntryListProps> = ({
  entries,
  onEdit,
  onDelete,
  onView,
  onGenerateFromReview,
  loading = false,
}) => {
  if (loading) {
    return (
      <div className="blog-list-loading">
        <div className="spinner-large"></div>
        <p>Loading blog entries...</p>
      </div>
    );
  }

  if (entries.length === 0) {
    return (
      <div className="blog-list-empty">
        <p>No blog entries yet. Create your first post to share your journey!</p>
        {onGenerateFromReview && (
          <Button
            variant="secondary"
            onClick={onGenerateFromReview}
            className="mt-2"
          >
            🎨 Generate from Daily Review
          </Button>
        )}
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const getStatusBadge = (status: string) => {
    const badges = {
      draft: { class: 'status-draft', label: 'Draft' },
      published: { class: 'status-published', label: 'Published' },
      archived: { class: 'status-archived', label: 'Archived' },
    };
    const badge = badges[status as keyof typeof badges] || badges.draft;
    return <span className={`status-badge ${badge.class}`}>{badge.label}</span>;
  };

  const truncateContent = (content: string, maxLength: number = 200) => {
    if (content.length <= maxLength) return content;
    return content.slice(0, maxLength).trim() + '...';
  };

  return (
    <div className="blog-list">
      {entries.map((entry) => (
        <div key={entry.id} className="blog-card">
          <div className="blog-card-header">
            <div className="blog-header-content">
              <h3 className="blog-title" onClick={() => onView(entry)}>
                {entry.title}
              </h3>
              <div className="blog-meta">
                {getStatusBadge(entry.status)}
                {entry.is_public && <span className="visibility-badge">🌐 Public</span>}
                {entry.is_featured && <span className="featured-badge">⭐ Featured</span>}
              </div>
            </div>
            <div className="blog-actions">
              <Button
                variant="secondary"
                onClick={() => onView(entry)}
                aria-label={`View ${entry.title}`}
              >
                View
              </Button>
              <Button
                variant="secondary"
                onClick={() => onEdit(entry)}
                aria-label={`Edit ${entry.title}`}
              >
                Edit
              </Button>
              <Button
                variant="danger"
                onClick={() => onDelete(entry.id)}
                aria-label={`Delete ${entry.title}`}
              >
                Delete
              </Button>
            </div>
          </div>

          {entry.excerpt && (
            <p className="blog-excerpt">{entry.excerpt}</p>
          )}

          {!entry.excerpt && entry.content && (
            <p className="blog-excerpt">{truncateContent(entry.content)}</p>
          )}

          <div className="blog-card-footer">
            <div className="blog-footer-info">
              {entry.published_at && (
                <span className="blog-date">📅 {formatDate(entry.published_at)}</span>
              )}
              {!entry.published_at && (
                <span className="blog-date">Created: {formatDate(entry.created_at)}</span>
              )}
              {entry.view_count > 0 && (
                <span className="blog-views">👁️ {entry.view_count} views</span>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default BlogEntryList;
