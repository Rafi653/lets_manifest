import React, { useState } from 'react';
import type {
  Workout,
  CreateWorkoutRequest,
  UpdateWorkoutRequest,
  CreateWorkoutExerciseRequest,
  WorkoutIntensity,
} from '../../types/workout';
import Button from '../common/Button';
import Input from '../common/Input';
import Select from '../common/Select';
import TextArea from '../common/TextArea';
import './WorkoutForm.css';

interface WorkoutFormProps {
  workout?: Workout;
  onSubmit: (data: CreateWorkoutRequest | UpdateWorkoutRequest) => Promise<void>;
  onCancel: () => void;
}

const WorkoutForm: React.FC<WorkoutFormProps> = ({ workout, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState<CreateWorkoutRequest>({
    workout_date: workout?.workout_date || new Date().toISOString().split('T')[0],
    workout_time: workout?.workout_time || '',
    workout_type: workout?.workout_type || '',
    workout_name: workout?.workout_name || '',
    duration_minutes: workout?.duration_minutes || undefined,
    calories_burned: workout?.calories_burned || undefined,
    intensity: workout?.intensity || undefined,
    location: workout?.location || '',
    notes: workout?.notes || '',
    mood_before: workout?.mood_before || '',
    mood_after: workout?.mood_after || '',
    exercises: workout?.exercises || [],
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    
    if (type === 'number') {
      const numValue = value === '' ? undefined : Number(value);
      setFormData((prev) => ({ ...prev, [name]: numValue }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value || undefined }));
    }
  };

  const addExercise = () => {
    const newExercise: CreateWorkoutExerciseRequest = {
      exercise_name: '',
      exercise_type: '',
      sets: undefined,
      reps: undefined,
      weight: undefined,
      weight_unit: 'lbs',
      distance: undefined,
      distance_unit: undefined,
      duration_seconds: undefined,
      rest_seconds: undefined,
      notes: '',
      order_index: formData.exercises?.length || 0,
    };
    setFormData((prev) => ({
      ...prev,
      exercises: [...(prev.exercises || []), newExercise],
    }));
  };

  const removeExercise = (index: number) => {
    setFormData((prev) => ({
      ...prev,
      exercises: prev.exercises?.filter((_, i) => i !== index),
    }));
  };

  const updateExercise = (index: number, field: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      exercises: prev.exercises?.map((ex, i) =>
        i === index ? { ...ex, [field]: value || undefined } : ex
      ),
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await onSubmit(formData);
    } catch (err) {
      console.error('Error submitting workout:', err);
      setError('Failed to save workout. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="workout-form" onSubmit={handleSubmit}>
      {error && <div className="error-message">{error}</div>}

      <div className="form-section">
        <h3>Workout Details</h3>
        <div className="form-row">
          <Input
            label="Date *"
            type="date"
            name="workout_date"
            value={formData.workout_date}
            onChange={handleChange}
            required
          />

          <Input
            label="Time"
            type="time"
            name="workout_time"
            value={formData.workout_time}
            onChange={handleChange}
          />

          <Input
            label="Workout Type *"
            type="text"
            name="workout_type"
            value={formData.workout_type}
            onChange={handleChange}
            placeholder="e.g., Strength, Cardio, HIIT"
            required
          />
        </div>

        <div className="form-row">
          <Input
            label="Workout Name"
            type="text"
            name="workout_name"
            value={formData.workout_name || ''}
            onChange={handleChange}
            placeholder="e.g., Upper Body Day"
          />

          <Input
            label="Duration (minutes)"
            type="number"
            name="duration_minutes"
            value={formData.duration_minutes || ''}
            onChange={handleChange}
            min="0"
          />

          <Select
            label="Intensity"
            name="intensity"
            value={formData.intensity || ''}
            onChange={handleChange}
          >
            <option value="">Select intensity</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </Select>
        </div>

        <div className="form-row">
          <Input
            label="Calories Burned"
            type="number"
            name="calories_burned"
            value={formData.calories_burned || ''}
            onChange={handleChange}
            min="0"
            step="0.01"
          />

          <Input
            label="Location"
            type="text"
            name="location"
            value={formData.location || ''}
            onChange={handleChange}
            placeholder="e.g., Home, Gym"
          />
        </div>

        <div className="form-row">
          <Input
            label="Mood Before"
            type="text"
            name="mood_before"
            value={formData.mood_before || ''}
            onChange={handleChange}
            placeholder="e.g., Tired, Energized"
          />

          <Input
            label="Mood After"
            type="text"
            name="mood_after"
            value={formData.mood_after || ''}
            onChange={handleChange}
            placeholder="e.g., Great, Accomplished"
          />
        </div>

        <TextArea
          label="Notes"
          name="notes"
          value={formData.notes || ''}
          onChange={handleChange}
          placeholder="Any additional notes about this workout..."
          rows={3}
        />
      </div>

      <div className="form-section">
        <div className="section-header">
          <h3>Exercises</h3>
          <Button type="button" variant="secondary" onClick={addExercise}>
            + Add Exercise
          </Button>
        </div>

        {formData.exercises && formData.exercises.length > 0 ? (
          <div className="exercises-list">
            {formData.exercises.map((exercise, index) => (
              <div key={index} className="exercise-item">
                <div className="exercise-header">
                  <span className="exercise-number">Exercise {index + 1}</span>
                  <Button
                    type="button"
                    variant="danger"
                    size="small"
                    onClick={() => removeExercise(index)}
                  >
                    Remove
                  </Button>
                </div>

                <div className="form-row">
                  <Input
                    label="Exercise Name *"
                    type="text"
                    value={exercise.exercise_name}
                    onChange={(e) => updateExercise(index, 'exercise_name', e.target.value)}
                    placeholder="e.g., Bench Press"
                    required
                  />

                  <Input
                    label="Exercise Type"
                    type="text"
                    value={exercise.exercise_type || ''}
                    onChange={(e) => updateExercise(index, 'exercise_type', e.target.value)}
                    placeholder="e.g., Compound, Isolation"
                  />
                </div>

                <div className="form-row">
                  <Input
                    label="Sets"
                    type="number"
                    value={exercise.sets || ''}
                    onChange={(e) => updateExercise(index, 'sets', e.target.value)}
                    min="0"
                  />

                  <Input
                    label="Reps"
                    type="number"
                    value={exercise.reps || ''}
                    onChange={(e) => updateExercise(index, 'reps', e.target.value)}
                    min="0"
                  />

                  <Input
                    label="Weight"
                    type="number"
                    value={exercise.weight || ''}
                    onChange={(e) => updateExercise(index, 'weight', e.target.value)}
                    min="0"
                    step="0.01"
                  />

                  <Select
                    label="Weight Unit"
                    value={exercise.weight_unit}
                    onChange={(e) => updateExercise(index, 'weight_unit', e.target.value)}
                  >
                    <option value="lbs">lbs</option>
                    <option value="kg">kg</option>
                  </Select>
                </div>

                <div className="form-row">
                  <Input
                    label="Distance"
                    type="number"
                    value={exercise.distance || ''}
                    onChange={(e) => updateExercise(index, 'distance', e.target.value)}
                    min="0"
                    step="0.01"
                  />

                  <Select
                    label="Distance Unit"
                    value={exercise.distance_unit || ''}
                    onChange={(e) => updateExercise(index, 'distance_unit', e.target.value)}
                  >
                    <option value="">Select unit</option>
                    <option value="miles">Miles</option>
                    <option value="km">Kilometers</option>
                    <option value="meters">Meters</option>
                  </Select>

                  <Input
                    label="Duration (seconds)"
                    type="number"
                    value={exercise.duration_seconds || ''}
                    onChange={(e) => updateExercise(index, 'duration_seconds', e.target.value)}
                    min="0"
                  />

                  <Input
                    label="Rest (seconds)"
                    type="number"
                    value={exercise.rest_seconds || ''}
                    onChange={(e) => updateExercise(index, 'rest_seconds', e.target.value)}
                    min="0"
                  />
                </div>

                <TextArea
                  label="Exercise Notes"
                  value={exercise.notes || ''}
                  onChange={(e) => updateExercise(index, 'notes', e.target.value)}
                  placeholder="Notes about this exercise..."
                  rows={2}
                />
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-exercises">
            <p>No exercises added yet. Click "Add Exercise" to start tracking.</p>
          </div>
        )}
      </div>

      <div className="form-actions">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={loading}>
          Cancel
        </Button>
        <Button type="submit" variant="primary" disabled={loading}>
          {loading ? 'Saving...' : workout ? 'Update' : 'Create'} Workout
        </Button>
      </div>
    </form>
  );
};

export default WorkoutForm;
