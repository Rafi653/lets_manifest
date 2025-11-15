import React, { useState, useEffect } from 'react';
import type { DailyReview, DailyReviewCreate, DailyReviewUpdate } from '../../types/dailyReview';
import { dailyReviewService } from '../../services/dailyReviewService';
import DailyReviewForm from '../../components/Review/DailyReviewForm';
import DailyReviewList from '../../components/Review/DailyReviewList';
import Button from '../../components/common/Button';
import './Review.css';

const Review: React.FC = () => {
  const [reviews, setReviews] = useState<DailyReview[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingReview, setEditingReview] = useState<DailyReview | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadReviews();
  }, []);

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

  const handleCreateReview = async (data: DailyReviewCreate | DailyReviewUpdate) => {
    try {
      await dailyReviewService.createReview(data as DailyReviewCreate);
      await loadReviews();
      setShowForm(false);
    } catch (err) {
      console.error('Failed to create review:', err);
      throw err;
    }
  };

  const handleUpdateReview = async (data: DailyReviewCreate | DailyReviewUpdate) => {
    if (!editingReview) return;

    try {
      await dailyReviewService.updateReview(editingReview.id, data as DailyReviewUpdate);
      await loadReviews();
      setEditingReview(undefined);
      setShowForm(false);
    } catch (err) {
      console.error('Failed to update review:', err);
      throw err;
    }
  };

  const handleDeleteReview = async (reviewId: string) => {
    if (!window.confirm('Are you sure you want to delete this review?')) {
      return;
    }

    try {
      await dailyReviewService.deleteReview(reviewId);
      await loadReviews();
    } catch (err) {
      console.error('Failed to delete review:', err);
      setError('Failed to delete review. Please try again.');
    }
  };

  const handleEditReview = (review: DailyReview) => {
    setEditingReview(review);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingReview(undefined);
  };

  const handleNewReview = () => {
    setEditingReview(undefined);
    setShowForm(true);
  };

  return (
    <div className="page-container review-page">
      <div className="page-header">
        <div>
          <h1>Daily Review</h1>
          <p>Reflect on your day, acknowledge your progress, and set intentions for tomorrow.</p>
        </div>
        {!showForm && (
          <Button onClick={handleNewReview} variant="primary">
            + New Review
          </Button>
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

      {showForm && (
        <div className="form-container">
          <h2>{editingReview ? 'Edit Daily Review' : 'Create New Daily Review'}</h2>
          <DailyReviewForm
            review={editingReview}
            onSubmit={editingReview ? handleUpdateReview : handleCreateReview}
            onCancel={handleCancelForm}
          />
        </div>
      )}

      {!showForm && (
        <DailyReviewList
          reviews={reviews}
          onEdit={handleEditReview}
          onDelete={handleDeleteReview}
          loading={loading}
        />
      )}
    </div>
  );
};

export default Review;
