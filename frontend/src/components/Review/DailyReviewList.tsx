/**
 * DailyReviewList component for displaying and managing daily reviews
 */

import React from 'react';
import type { DailyReview } from '../../types/dailyReview';
import Button from '../common/Button';
import './DailyReviewList.css';

interface DailyReviewListProps {
  reviews: DailyReview[];
  onEdit: (review: DailyReview) => void;
  onDelete: (reviewId: string) => void;
  loading?: boolean;
}

const DailyReviewList: React.FC<DailyReviewListProps> = ({
  reviews,
  onEdit,
  onDelete,
  loading = false,
}) => {
  if (loading) {
    return (
      <div className="review-list-loading">
        <div className="spinner-large"></div>
        <p>Loading reviews...</p>
      </div>
    );
  }

  if (reviews.length === 0) {
    return (
      <div className="review-list-empty">
        <p>No reviews yet. Create your first daily review to get started!</p>
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

  const renderRating = (value: number | null, label: string) => {
    if (value === null) return null;
    return (
      <div className="metric-item">
        <span className="metric-label">{label}:</span>
        <div className="rating-bar">
          <div
            className="rating-fill"
            style={{ width: `${(value / 10) * 100}%` }}
            role="progressbar"
            aria-valuenow={value}
            aria-valuemin={1}
            aria-valuemax={10}
            aria-label={`${label}: ${value} out of 10`}
          />
          <span className="rating-value">{value}/10</span>
        </div>
      </div>
    );
  };

  return (
    <div className="review-list">
      {reviews.map((review) => (
        <div key={review.id} className="review-card">
          <div className="review-card-header">
            <div>
              <h3 className="review-date">{formatDate(review.review_date)}</h3>
            </div>
            <div className="review-actions">
              <Button
                variant="secondary"
                onClick={() => onEdit(review)}
                aria-label={`Edit review for ${formatDate(review.review_date)}`}
              >
                Edit
              </Button>
              <Button
                variant="danger"
                onClick={() => onDelete(review.id)}
                aria-label={`Delete review for ${formatDate(review.review_date)}`}
              >
                Delete
              </Button>
            </div>
          </div>

          {/* Metrics Section */}
          <div className="review-metrics">
            {renderRating(review.mood_rating, 'Mood')}
            {renderRating(review.energy_level, 'Energy')}
            {renderRating(review.productivity_rating, 'Productivity')}
            {renderRating(review.sleep_quality, 'Sleep Quality')}

            {review.sleep_hours !== null && (
              <div className="metric-item">
                <span className="metric-label">Sleep:</span>
                <span className="metric-value">{review.sleep_hours}h</span>
              </div>
            )}

            {review.water_intake_ml !== null && (
              <div className="metric-item">
                <span className="metric-label">Water:</span>
                <span className="metric-value">{review.water_intake_ml}ml</span>
              </div>
            )}

            {review.screen_time_minutes !== null && (
              <div className="metric-item">
                <span className="metric-label">Screen Time:</span>
                <span className="metric-value">
                  {Math.floor(review.screen_time_minutes / 60)}h {review.screen_time_minutes % 60}m
                </span>
              </div>
            )}

            {review.steps !== null && (
              <div className="metric-item">
                <span className="metric-label">Steps:</span>
                <span className="metric-value">{review.steps.toLocaleString()}</span>
              </div>
            )}
          </div>

          {/* Reflections Section */}
          <div className="review-reflections">
            {review.accomplishments && (
              <div className="reflection-item">
                <h4 className="reflection-title">✅ Accomplishments</h4>
                <p className="reflection-text">{review.accomplishments}</p>
              </div>
            )}

            {review.challenges && (
              <div className="reflection-item">
                <h4 className="reflection-title">🚧 Challenges</h4>
                <p className="reflection-text">{review.challenges}</p>
              </div>
            )}

            {review.lessons_learned && (
              <div className="reflection-item">
                <h4 className="reflection-title">💡 Lessons Learned</h4>
                <p className="reflection-text">{review.lessons_learned}</p>
              </div>
            )}

            {review.gratitude && (
              <div className="reflection-item">
                <h4 className="reflection-title">🙏 Gratitude</h4>
                <p className="reflection-text">{review.gratitude}</p>
              </div>
            )}

            {review.tomorrow_intentions && (
              <div className="reflection-item">
                <h4 className="reflection-title">🎯 Tomorrow's Intentions</h4>
                <p className="reflection-text">{review.tomorrow_intentions}</p>
              </div>
            )}

            {review.highlights && (
              <div className="reflection-item">
                <h4 className="reflection-title">⭐ Highlights</h4>
                <p className="reflection-text">{review.highlights}</p>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default DailyReviewList;
