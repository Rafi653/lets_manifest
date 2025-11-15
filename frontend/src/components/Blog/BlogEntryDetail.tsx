/**
 * BlogEntryDetail component for viewing a single blog entry
 */

import React from 'react';
import type { BlogEntry } from '../../types/blogEntry';
import Button from '../common/Button';
import './BlogEntryDetail.css';

interface BlogEntryDetailProps {
  entry: BlogEntry;
  onEdit: (entry: BlogEntry) => void;
  onDelete: (entryId: string) => void;
  onBack: () => void;
}

const BlogEntryDetail: React.FC<BlogEntryDetailProps> = ({
  entry,
  onEdit,
  onDelete,
  onBack,
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
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

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this blog entry?')) {
      onDelete(entry.id);
    }
  };

  return (
    <div className="blog-detail">
      <div className="blog-detail-header">
        <Button variant="secondary" onClick={onBack}>
          ← Back to List
        </Button>
        <div className="blog-detail-actions">
          <Button variant="secondary" onClick={() => onEdit(entry)}>
            Edit
          </Button>
          <Button variant="danger" onClick={handleDelete}>
            Delete
          </Button>
        </div>
      </div>

      <article className="blog-detail-content">
        <div className="blog-detail-meta">
          {getStatusBadge(entry.status)}
          {entry.is_public && <span className="visibility-badge">🌐 Public</span>}
          {entry.is_featured && <span className="featured-badge">⭐ Featured</span>}
        </div>

        <h1 className="blog-detail-title">{entry.title}</h1>

        <div className="blog-detail-info">
          {entry.published_at && (
            <span className="info-item">
              📅 Published: {formatDate(entry.published_at)}
            </span>
          )}
          {!entry.published_at && (
            <span className="info-item">
              📅 Created: {formatDate(entry.created_at)}
            </span>
          )}
          {entry.updated_at && entry.updated_at !== entry.created_at && (
            <span className="info-item">
              ✏️ Updated: {formatDate(entry.updated_at)}
            </span>
          )}
          {entry.view_count > 0 && (
            <span className="info-item">
              👁️ {entry.view_count} views
            </span>
          )}
        </div>

        {entry.excerpt && (
          <div className="blog-detail-excerpt">
            <strong>Summary:</strong> {entry.excerpt}
          </div>
        )}

        <div className="blog-detail-body">
          {entry.content.split('\n').map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>
      </article>
    </div>
  );
};

export default BlogEntryDetail;
