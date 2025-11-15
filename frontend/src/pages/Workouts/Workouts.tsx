import React, { useState, useEffect } from 'react';
import type { Workout, CreateWorkoutRequest, UpdateWorkoutRequest } from '../../types/workout';
import { workoutService } from '../../services/workoutService';
import WorkoutForm from '../../components/Workouts/WorkoutForm';
import WorkoutList from '../../components/Workouts/WorkoutList';
import Button from '../../components/common/Button';
import Select from '../../components/common/Select';
import Input from '../../components/common/Input';
import './Workouts.css';

const Workouts: React.FC = () => {
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingWorkout, setEditingWorkout] = useState<Workout | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [workoutTypeFilter, setWorkoutTypeFilter] = useState<string>('');
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  useEffect(() => {
    loadWorkouts();
  }, [workoutTypeFilter, startDate, endDate, page]);

  const loadWorkouts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await workoutService.getWorkouts(
        workoutTypeFilter || undefined,
        startDate || undefined,
        endDate || undefined,
        page,
        20
      );
      setWorkouts(data.items);
      setTotalPages(data.total_pages);
    } catch (err) {
      console.error('Failed to load workouts:', err);
      setError('Failed to load workouts. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateWorkout = async (data: CreateWorkoutRequest | UpdateWorkoutRequest) => {
    try {
      await workoutService.createWorkout(data as CreateWorkoutRequest);
      await loadWorkouts();
      setShowForm(false);
    } catch (err) {
      console.error('Failed to create workout:', err);
      throw err;
    }
  };

  const handleUpdateWorkout = async (data: CreateWorkoutRequest | UpdateWorkoutRequest) => {
    if (!editingWorkout) return;

    try {
      await workoutService.updateWorkout(editingWorkout.id, data as UpdateWorkoutRequest);
      await loadWorkouts();
      setEditingWorkout(undefined);
      setShowForm(false);
    } catch (err) {
      console.error('Failed to update workout:', err);
      throw err;
    }
  };

  const handleDeleteWorkout = async (workoutId: string) => {
    if (!window.confirm('Are you sure you want to delete this workout?')) {
      return;
    }

    try {
      await workoutService.deleteWorkout(workoutId);
      await loadWorkouts();
    } catch (err) {
      console.error('Failed to delete workout:', err);
      setError('Failed to delete workout. Please try again.');
    }
  };

  const handleEditWorkout = (workout: Workout) => {
    setEditingWorkout(workout);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingWorkout(undefined);
  };

  const handleNewWorkout = () => {
    setEditingWorkout(undefined);
    setShowForm(true);
  };

  const clearFilters = () => {
    setWorkoutTypeFilter('');
    setStartDate('');
    setEndDate('');
    setPage(1);
  };

  // Calculate workout stats
  const stats = workouts.reduce(
    (acc, workout) => ({
      total_workouts: acc.total_workouts + 1,
      total_duration: acc.total_duration + (workout.duration_minutes || 0),
      total_calories: acc.total_calories + (workout.calories_burned || 0),
      total_exercises: acc.total_exercises + (workout.exercises?.length || 0),
    }),
    { total_workouts: 0, total_duration: 0, total_calories: 0, total_exercises: 0 }
  );

  return (
    <div className="page-container workouts-page">
      <div className="page-header">
        <div>
          <h1>Workouts</h1>
          <p>Track your fitness activities and exercise routines to stay healthy and strong.</p>
        </div>
        {!showForm && (
          <Button onClick={handleNewWorkout} variant="primary">
            + Log Workout
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
          <h2>{editingWorkout ? 'Edit Workout' : 'Log New Workout'}</h2>
          <WorkoutForm
            workout={editingWorkout}
            onSubmit={editingWorkout ? handleUpdateWorkout : handleCreateWorkout}
            onCancel={handleCancelForm}
          />
        </div>
      )}

      {!showForm && (
        <>
          {workouts.length > 0 && (
            <div className="workout-summary">
              <h3>Workout Summary</h3>
              <div className="summary-stats">
                <div className="summary-stat">
                  <div className="stat-value">{stats.total_workouts}</div>
                  <div className="stat-label">Total Workouts</div>
                </div>
                <div className="summary-stat">
                  <div className="stat-value">{stats.total_duration}</div>
                  <div className="stat-label">Minutes</div>
                </div>
                <div className="summary-stat">
                  <div className="stat-value">{Math.round(stats.total_calories)}</div>
                  <div className="stat-label">Calories Burned</div>
                </div>
                <div className="summary-stat">
                  <div className="stat-value">{stats.total_exercises}</div>
                  <div className="stat-label">Exercises</div>
                </div>
              </div>
            </div>
          )}

          <div className="filters-container">
            <div className="filters">
              <Input
                label="Workout Type"
                type="text"
                value={workoutTypeFilter}
                onChange={(e) => {
                  setWorkoutTypeFilter(e.target.value);
                  setPage(1);
                }}
                placeholder="e.g., Strength, Cardio"
              />

              <Input
                label="Start Date"
                type="date"
                value={startDate}
                onChange={(e) => {
                  setStartDate(e.target.value);
                  setPage(1);
                }}
              />

              <Input
                label="End Date"
                type="date"
                value={endDate}
                onChange={(e) => {
                  setEndDate(e.target.value);
                  setPage(1);
                }}
              />

              <Button variant="secondary" onClick={clearFilters}>
                Clear Filters
              </Button>
            </div>
          </div>

          <WorkoutList
            workouts={workouts}
            onEdit={handleEditWorkout}
            onDelete={handleDeleteWorkout}
            loading={loading}
          />

          {totalPages > 1 && (
            <div className="pagination">
              <Button
                variant="secondary"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
              >
                Previous
              </Button>
              <span className="page-info">
                Page {page} of {totalPages}
              </span>
              <Button
                variant="secondary"
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
              >
                Next
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Workouts;
