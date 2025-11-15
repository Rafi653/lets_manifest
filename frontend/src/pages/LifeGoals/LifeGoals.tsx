import React, { useState, useEffect } from 'react';
import type { Goal, GoalCreate, GoalUpdate, LifeGoalSummary } from '../../types/goal';
import { lifeGoalService } from '../../services/lifeGoalService';
import LifeGoalForm from '../../components/LifeGoals/LifeGoalForm';
import LifeGoalList from '../../components/LifeGoals/LifeGoalList';
import LifeGoalAnalytics from '../../components/LifeGoals/LifeGoalAnalytics';
import Button from '../../components/common/Button';
import './LifeGoals.css';

const LifeGoals: React.FC = () => {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingGoal, setEditingGoal] = useState<Goal | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<LifeGoalSummary | null>(null);
  const [showAnalytics, setShowAnalytics] = useState(false);

  useEffect(() => {
    loadLifeGoals();
    loadSummary();
  }, []);

  const loadLifeGoals = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await lifeGoalService.getLifeGoals();
      setGoals(data.items);
    } catch (err) {
      console.error('Failed to load life goals:', err);
      setError('Failed to load life goals. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadSummary = async () => {
    try {
      const summaryData = await lifeGoalService.getLifeGoalSummary();
      setSummary(summaryData);
    } catch (err) {
      console.error('Failed to load summary:', err);
    }
  };

  const handleCreateGoal = async (data: GoalCreate | GoalUpdate) => {
    try {
      await lifeGoalService.createLifeGoal(data as GoalCreate);
      await loadLifeGoals();
      await loadSummary();
      setShowForm(false);
    } catch (err) {
      console.error('Failed to create life goal:', err);
      throw err;
    }
  };

  const handleUpdateGoal = async (data: GoalCreate | GoalUpdate) => {
    if (!editingGoal) return;

    try {
      await lifeGoalService.updateLifeGoal(editingGoal.id, data as GoalUpdate);
      await loadLifeGoals();
      await loadSummary();
      setEditingGoal(undefined);
      setShowForm(false);
    } catch (err) {
      console.error('Failed to update life goal:', err);
      throw err;
    }
  };

  const handleDeleteGoal = async (goalId: string) => {
    if (!window.confirm('Are you sure you want to delete this life goal?')) {
      return;
    }

    try {
      await lifeGoalService.deleteLifeGoal(goalId);
      await loadLifeGoals();
      await loadSummary();
    } catch (err) {
      console.error('Failed to delete life goal:', err);
      setError('Failed to delete life goal. Please try again.');
    }
  };

  const handleEditGoal = (goal: Goal) => {
    setEditingGoal(goal);
    setShowForm(true);
    setShowAnalytics(false);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingGoal(undefined);
  };

  const handleNewGoal = () => {
    setEditingGoal(undefined);
    setShowForm(true);
    setShowAnalytics(false);
  };

  const toggleAnalytics = () => {
    setShowAnalytics(!showAnalytics);
    setShowForm(false);
  };

  return (
    <div className="page-container life-goals-page">
      <div className="page-header">
        <div>
          <h1>Life Goals</h1>
          <p>
            Track your long-term aspirations across different life areas. Set milestones and
            monitor your progress towards meaningful life achievements.
          </p>
        </div>
        <div className="header-actions">
          {!showForm && !showAnalytics && (
            <Button onClick={handleNewGoal} variant="primary">
              + New Life Goal
            </Button>
          )}
          <Button 
            onClick={toggleAnalytics} 
            variant={showAnalytics ? "primary" : "secondary"}
          >
            {showAnalytics ? 'View Goals' : 'View Analytics'}
          </Button>
        </div>
      </div>

      {summary && !showForm && !showAnalytics && (
        <div className="summary-cards">
          <div className="summary-card">
            <div className="summary-value">{summary.total_goals}</div>
            <div className="summary-label">Total Goals</div>
          </div>
          <div className="summary-card">
            <div className="summary-value">{summary.active_goals}</div>
            <div className="summary-label">Active</div>
          </div>
          <div className="summary-card">
            <div className="summary-value">{summary.completed_goals}</div>
            <div className="summary-label">Completed</div>
          </div>
          <div className="summary-card">
            <div className="summary-value">{summary.completion_rate}%</div>
            <div className="summary-label">Completion Rate</div>
          </div>
        </div>
      )}

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
          <h2>{editingGoal ? 'Edit Life Goal' : 'Create New Life Goal'}</h2>
          <LifeGoalForm
            goal={editingGoal}
            onSubmit={editingGoal ? handleUpdateGoal : handleCreateGoal}
            onCancel={handleCancelForm}
          />
        </div>
      )}

      {showAnalytics && (
        <LifeGoalAnalytics />
      )}

      {!showForm && !showAnalytics && (
        <LifeGoalList
          goals={goals}
          onEdit={handleEditGoal}
          onDelete={handleDeleteGoal}
          loading={loading}
        />
      )}
    </div>
  );
};

export default LifeGoals;
