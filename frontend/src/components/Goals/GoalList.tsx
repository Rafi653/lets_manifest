/**
 * GoalList component for displaying and managing goals
 */

import React from 'react';
import type { Goal } from '../../types/goal';
import Button from '../common/Button';
import './GoalList.css';

interface GoalListProps {
  goals: Goal[];
  onEdit: (goal: Goal) => void;
  onDelete: (goalId: string) => void;
  loading?: boolean;
}

const GoalList: React.FC<GoalListProps> = ({ goals, onEdit, onDelete, loading = false }) => {
  if (loading) {
    return (
      <div className="goal-list-loading">
        <div className="spinner-large"></div>
        <p>Loading goals...</p>
      </div>
    );
  }

  if (goals.length === 0) {
    return (
      <div className="goal-list-empty">
        <p>No goals yet. Create your first goal to get started!</p>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getProgressPercentage = (goal: Goal): number => {
    if (!goal.target_value) return 0;
    return Math.min(100, (goal.current_value / goal.target_value) * 100);
  };

  const getStatusBadgeClass = (status: string): string => {
    switch (status) {
      case 'active':
        return 'badge-active';
      case 'completed':
        return 'badge-completed';
      case 'paused':
        return 'badge-paused';
      case 'cancelled':
        return 'badge-cancelled';
      default:
        return '';
    }
  };

  const getPriorityLabel = (priority: number): string => {
    const labels = ['None', 'Low', 'Medium-Low', 'Medium', 'Medium-High', 'High'];
    return labels[priority] || 'None';
  };

  return (
    <div className="goal-list">
      {goals.map((goal) => (
        <div key={goal.id} className="goal-card">
          <div className="goal-card-header">
            <div className="goal-header-left">
              <h3 className="goal-title">{goal.title}</h3>
              <div className="goal-badges">
                <span className={`badge ${getStatusBadgeClass(goal.status)}`}>
                  {goal.status}
                </span>
                <span className="badge badge-type">{goal.goal_type}</span>
                {goal.priority > 0 && (
                  <span className="badge badge-priority">
                    Priority: {getPriorityLabel(goal.priority)}
                  </span>
                )}
              </div>
            </div>
            <div className="goal-actions">
              <Button
                variant="secondary"
                onClick={() => onEdit(goal)}
                aria-label={`Edit ${goal.title}`}
              >
                Edit
              </Button>
              <Button
                variant="danger"
                onClick={() => onDelete(goal.id)}
                aria-label={`Delete ${goal.title}`}
              >
                Delete
              </Button>
            </div>
          </div>

          {goal.description && (
            <p className="goal-description">{goal.description}</p>
          )}

          {goal.category && (
            <p className="goal-category">
              <strong>Category:</strong> {goal.category}
            </p>
          )}

          {goal.target_value && (
            <div className="goal-progress">
              <div className="progress-info">
                <span>
                  Progress: {goal.current_value} / {goal.target_value}{' '}
                  {goal.target_unit || ''}
                </span>
                <span>{getProgressPercentage(goal).toFixed(0)}%</span>
              </div>
              <div className="progress-bar">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${getProgressPercentage(goal)}%` }}
                  role="progressbar"
                  aria-valuenow={getProgressPercentage(goal)}
                  aria-valuemin={0}
                  aria-valuemax={100}
                />
              </div>
            </div>
          )}

          <div className="goal-dates">
            <span>
              <strong>Start:</strong> {formatDate(goal.start_date)}
            </span>
            <span>
              <strong>End:</strong> {formatDate(goal.end_date)}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default GoalList;
