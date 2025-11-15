import React, { useState, useEffect } from 'react';
import type { Goal, GoalCreate, GoalUpdate } from '../../types/goal';
import { goalService } from '../../services/goalService';
import GoalForm from '../../components/Goals/GoalForm';
import GoalList from '../../components/Goals/GoalList';
import Button from '../../components/common/Button';
import './Goals.css';

const Goals: React.FC = () => {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingGoal, setEditingGoal] = useState<Goal | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadGoals();
  }, []);

  const loadGoals = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await goalService.getGoals();
      setGoals(data.items);
    } catch (err) {
      console.error('Failed to load goals:', err);
      setError('Failed to load goals. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateGoal = async (data: GoalCreate | GoalUpdate) => {
    try {
      await goalService.createGoal(data as GoalCreate);
      await loadGoals();
      setShowForm(false);
    } catch (err) {
      console.error('Failed to create goal:', err);
      throw err;
    }
  };

  const handleUpdateGoal = async (data: GoalCreate | GoalUpdate) => {
    if (!editingGoal) return;

    try {
      await goalService.updateGoal(editingGoal.id, data as GoalUpdate);
      await loadGoals();
      setEditingGoal(undefined);
      setShowForm(false);
    } catch (err) {
      console.error('Failed to update goal:', err);
      throw err;
    }
  };

  const handleDeleteGoal = async (goalId: string) => {
    if (!window.confirm('Are you sure you want to delete this goal?')) {
      return;
    }

    try {
      await goalService.deleteGoal(goalId);
      await loadGoals();
    } catch (err) {
      console.error('Failed to delete goal:', err);
      setError('Failed to delete goal. Please try again.');
    }
  };

  const handleEditGoal = (goal: Goal) => {
    setEditingGoal(goal);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingGoal(undefined);
  };

  const handleNewGoal = () => {
    setEditingGoal(undefined);
    setShowForm(true);
  };

  return (
    <div className="page-container goals-page">
      <div className="page-header">
        <div>
          <h1>Goals</h1>
          <p>Set and track your manifestation goals. Define your intentions and watch them come to life.</p>
        </div>
        {!showForm && (
          <Button onClick={handleNewGoal} variant="primary">
            + New Goal
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
          <h2>{editingGoal ? 'Edit Goal' : 'Create New Goal'}</h2>
          <GoalForm
            goal={editingGoal}
            onSubmit={editingGoal ? handleUpdateGoal : handleCreateGoal}
            onCancel={handleCancelForm}
          />
        </div>
      )}

      {!showForm && (
        <GoalList
          goals={goals}
          onEdit={handleEditGoal}
          onDelete={handleDeleteGoal}
          loading={loading}
        />
      )}
    </div>
  );
};

export default Goals;
