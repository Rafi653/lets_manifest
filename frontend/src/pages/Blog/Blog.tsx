import React, { useState, useEffect } from 'react';
import type { BlogEntry, BlogEntryCreate, BlogEntryUpdate } from '../../types/blogEntry';
import type { DailyReview } from '../../types/dailyReview';
import { blogEntryService } from '../../services/blogEntryService';
import { dailyReviewService } from '../../services/dailyReviewService';
import BlogEntryForm from '../../components/Blog/BlogEntryForm';
import BlogEntryList from '../../components/Blog/BlogEntryList';
import BlogEntryDetail from '../../components/Blog/BlogEntryDetail';
import Button from '../../components/common/Button';
import './Blog.css';

type ViewMode = 'list' | 'form' | 'detail' | 'review-select';

const Blog: React.FC = () => {
  const [entries, setEntries] = useState<BlogEntry[]>([]);
  const [reviews, setReviews] = useState<DailyReview[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<ViewMode>('list');
  const [editingEntry, setEditingEntry] = useState<BlogEntry | undefined>(undefined);
  const [viewingEntry, setViewingEntry] = useState<BlogEntry | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadEntries();
  }, []);

  const loadEntries = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await blogEntryService.getBlogEntries();
      setEntries(data.items);
    } catch (err) {
      console.error('Failed to load blog entries:', err);
      setError('Failed to load blog entries. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadReviews = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await dailyReviewService.getReviews();
      setReviews(data.items);
    } catch (err) {
      console.error('Failed to load reviews:', err);
      setError('Failed to load reviews. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateEntry = async (data: BlogEntryCreate | BlogEntryUpdate) => {
    try {
      await blogEntryService.createBlogEntry(data as BlogEntryCreate);
      await loadEntries();
      setViewMode('list');
    } catch (err) {
      console.error('Failed to create entry:', err);
      throw err;
    }
  };

  const handleUpdateEntry = async (data: BlogEntryCreate | BlogEntryUpdate) => {
    if (!editingEntry) return;

    try {
      await blogEntryService.updateBlogEntry(editingEntry.id, data as BlogEntryUpdate);
      await loadEntries();
      setEditingEntry(undefined);
      setViewMode('list');
    } catch (err) {
      console.error('Failed to update entry:', err);
      throw err;
    }
  };

  const handleDeleteEntry = async (entryId: string) => {
    if (!window.confirm('Are you sure you want to delete this blog entry?')) {
      return;
    }

    try {
      await blogEntryService.deleteBlogEntry(entryId);
      await loadEntries();
      if (viewingEntry?.id === entryId) {
        setViewingEntry(undefined);
        setViewMode('list');
      }
    } catch (err) {
      console.error('Failed to delete entry:', err);
      setError('Failed to delete entry. Please try again.');
    }
  };

  const handleEditEntry = (entry: BlogEntry) => {
    setEditingEntry(entry);
    setViewMode('form');
  };

  const handleViewEntry = (entry: BlogEntry) => {
    setViewingEntry(entry);
    setViewMode('detail');
  };

  const handleCancelForm = () => {
    setViewMode('list');
    setEditingEntry(undefined);
  };

  const handleNewEntry = () => {
    setEditingEntry(undefined);
    setViewMode('form');
  };

  const handleGenerateFromReview = () => {
    loadReviews();
    setViewMode('review-select');
  };

  const handleSelectReview = async (review: DailyReview) => {
    try {
      setLoading(true);
      const entry = await blogEntryService.generateFromReview(review.id);
      await loadEntries();
      setEditingEntry(entry);
      setViewMode('form');
    } catch (err) {
      console.error('Failed to generate blog from review:', err);
      setError('Failed to generate blog entry. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="page-container blog-page">
      <div className="page-header">
        <div>
          <h1>Blog</h1>
          <p>Share your manifestation journey through personal blog entries and reflections.</p>
        </div>
        {viewMode === 'list' && (
          <div className="header-actions">
            <Button onClick={handleGenerateFromReview} variant="secondary">
              🎨 Generate from Review
            </Button>
            <Button onClick={handleNewEntry} variant="primary">
              + New Blog Entry
            </Button>
          </div>
        )}
      </div>

      {error && (
        <div className="error-banner" role="alert">
          {error}
          <button
            className="error-close"
            onClick={() => setError(null)}
            aria-label="Dismiss error"
          >
            ×
          </button>
        </div>
      )}

      {viewMode === 'form' && (
        <div className="form-container">
          <h2>{editingEntry ? 'Edit Blog Entry' : 'Create New Blog Entry'}</h2>
          <BlogEntryForm
            entry={editingEntry}
            onSubmit={editingEntry ? handleUpdateEntry : handleCreateEntry}
            onCancel={handleCancelForm}
          />
        </div>
      )}

      {viewMode === 'detail' && viewingEntry && (
        <BlogEntryDetail
          entry={viewingEntry}
          onEdit={handleEditEntry}
          onDelete={handleDeleteEntry}
          onBack={() => setViewMode('list')}
        />
      )}

      {viewMode === 'review-select' && (
        <div className="review-select-container">
          <div className="review-select-header">
            <h2>Select a Daily Review to Generate Blog</h2>
            <Button onClick={() => setViewMode('list')} variant="secondary">
              Cancel
            </Button>
          </div>
          {loading ? (
            <div className="loading-container">
              <div className="spinner-large"></div>
              <p>Loading reviews...</p>
            </div>
          ) : reviews.length === 0 ? (
            <div className="empty-reviews">
              <p>No daily reviews found. Create a daily review first!</p>
            </div>
          ) : (
            <div className="review-grid">
              {reviews.map((review) => (
                <div key={review.id} className="review-card-compact">
                  <h3>{formatDate(review.review_date)}</h3>
                  {review.highlights && (
                    <p className="review-preview">{review.highlights.substring(0, 100)}...</p>
                  )}
                  <Button
                    variant="primary"
                    onClick={() => handleSelectReview(review)}
                  >
                    Generate Blog
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {viewMode === 'list' && (
        <BlogEntryList
          entries={entries}
          onEdit={handleEditEntry}
          onDelete={handleDeleteEntry}
          onView={handleViewEntry}
          onGenerateFromReview={handleGenerateFromReview}
          loading={loading}
        />
      )}
    </div>
  );
};

export default Blog;
