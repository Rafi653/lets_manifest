import React from 'react';
import type { Workout } from '../../types/workout';
import Button from '../common/Button';
import './WorkoutList.css';

interface WorkoutListProps {
  workouts: Workout[];
  onEdit: (workout: Workout) => void;
  onDelete: (workoutId: string) => void;
  loading?: boolean;
}

const WorkoutList: React.FC<WorkoutListProps> = ({ workouts, onEdit, onDelete, loading }) => {
  if (loading) {
    return <div className="loading">Loading workouts...</div>;
  }

  if (workouts.length === 0) {
    return (
      <div className="empty-state">
        <p>No workouts yet. Start tracking your fitness journey!</p>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const formatTime = (timeString?: string) => {
    if (!timeString) return '';
    try {
      const [hours, minutes] = timeString.split(':');
      const hour = parseInt(hours, 10);
      const ampm = hour >= 12 ? 'PM' : 'AM';
      const displayHour = hour % 12 || 12;
      return `${displayHour}:${minutes} ${ampm}`;
    } catch {
      return timeString;
    }
  };

  const getIntensityColor = (intensity?: string) => {
    const colors: Record<string, string> = {
      low: '#4caf50',
      medium: '#ff9800',
      high: '#f44336',
    };
    return colors[intensity || ''] || '#757575';
  };

  return (
    <div className="workout-list">
      {workouts.map((workout) => (
        <div key={workout.id} className="workout-card">
          <div className="workout-header">
            <div className="workout-title">
              <h3>{workout.workout_name || workout.workout_type}</h3>
              <div className="workout-meta">
                <span className="date">{formatDate(workout.workout_date)}</span>
                {workout.workout_time && (
                  <span className="time">{formatTime(workout.workout_time)}</span>
                )}
              </div>
            </div>
            <div className="workout-actions">
              <Button variant="secondary" size="small" onClick={() => onEdit(workout)}>
                Edit
              </Button>
              <Button variant="danger" size="small" onClick={() => onDelete(workout.id)}>
                Delete
              </Button>
            </div>
          </div>

          <div className="workout-details">
            <div className="detail-row">
              <span className="detail-label">Type:</span>
              <span className="detail-value">{workout.workout_type}</span>
            </div>
            
            {workout.intensity && (
              <div className="detail-row">
                <span className="detail-label">Intensity:</span>
                <span
                  className="intensity-badge"
                  style={{ backgroundColor: getIntensityColor(workout.intensity) }}
                >
                  {workout.intensity}
                </span>
              </div>
            )}

            {workout.duration_minutes && (
              <div className="detail-row">
                <span className="detail-label">Duration:</span>
                <span className="detail-value">{workout.duration_minutes} min</span>
              </div>
            )}

            {workout.calories_burned && (
              <div className="detail-row">
                <span className="detail-label">Calories:</span>
                <span className="detail-value">{Math.round(workout.calories_burned)} kcal</span>
              </div>
            )}

            {workout.location && (
              <div className="detail-row">
                <span className="detail-label">Location:</span>
                <span className="detail-value">{workout.location}</span>
              </div>
            )}

            {(workout.mood_before || workout.mood_after) && (
              <div className="detail-row">
                <span className="detail-label">Mood:</span>
                <span className="detail-value">
                  {workout.mood_before && `Before: ${workout.mood_before}`}
                  {workout.mood_before && workout.mood_after && ' → '}
                  {workout.mood_after && `After: ${workout.mood_after}`}
                </span>
              </div>
            )}
          </div>

          {workout.exercises && workout.exercises.length > 0 && (
            <div className="workout-exercises">
              <h4>Exercises ({workout.exercises.length})</h4>
              <div className="exercises-grid">
                {workout.exercises.map((exercise, idx) => (
                  <div key={exercise.id} className="exercise-card">
                    <div className="exercise-name">{exercise.exercise_name}</div>
                    <div className="exercise-details">
                      {exercise.sets && exercise.reps && (
                        <span>{exercise.sets} × {exercise.reps}</span>
                      )}
                      {exercise.weight && (
                        <span>{exercise.weight} {exercise.weight_unit}</span>
                      )}
                      {exercise.distance && (
                        <span>{exercise.distance} {exercise.distance_unit}</span>
                      )}
                      {exercise.duration_seconds && (
                        <span>{Math.round(exercise.duration_seconds / 60)} min</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {workout.notes && (
            <div className="workout-notes">
              <strong>Notes:</strong> {workout.notes}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default WorkoutList;
