import React, { useState, useEffect } from 'react';
import type { Goal, GoalCreate, GoalUpdate, LifeArea } from '../../types/goal';
import { LIFE_AREAS } from '../../types/goal';
import Button from '../common/Button';
import Input from '../common/Input';
import Select from '../common/Select';
import TextArea from '../common/TextArea';
import './LifeGoalForm.css';

interface LifeGoalFormProps {
  goal?: Goal;
  onSubmit: (data: GoalCreate | GoalUpdate) => Promise<void>;
  onCancel: () => void;
}

const LifeGoalForm: React.FC<LifeGoalFormProps> = ({ goal, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState<GoalCreate | GoalUpdate>({
    title: goal?.title || '',
    description: goal?.description || '',
    goal_type: 'life_goal',
    category: goal?.category || '',
    priority: goal?.priority || 3,
    status: goal?.status || 'active',
    target_value: goal?.target_value || null,
    target_unit: goal?.target_unit || '',
    start_date: goal?.start_date || null,
    end_date: goal?.end_date || null,
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.title?.trim()) {
      setError('Title is required');
      return;
    }

    if (!formData.category) {
      setError('Life area is required');
      return;
    }

    try {
      setSubmitting(true);
      setError(null);
      await onSubmit(formData);
    } catch (err) {
      console.error('Failed to submit form:', err);
      setError('Failed to save life goal. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? (value ? Number(value) : null) : value || null,
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="life-goal-form">
      {error && (
        <div className="form-error" role="alert">
          {error}
        </div>
      )}

      <div className="form-row">
        <div className="form-group full-width">
          <Input
            label="Goal Title"
            name="title"
            value={formData.title || ''}
            onChange={handleChange}
            placeholder="e.g., Buy my first investment property"
            required
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <Select
            label="Life Area"
            name="category"
            value={formData.category || ''}
            onChange={handleChange}
            required
          >
            <option value="">Select a life area...</option>
            {LIFE_AREAS.map(area => (
              <option key={area} value={area}>
                {area.charAt(0).toUpperCase() + area.slice(1).replace('_', ' ')}
              </option>
            ))}
          </Select>
        </div>

        <div className="form-group">
          <Select
            label="Priority"
            name="priority"
            value={formData.priority?.toString() || '3'}
            onChange={handleChange}
          >
            <option value="1">Low (1)</option>
            <option value="2">Medium-Low (2)</option>
            <option value="3">Medium (3)</option>
            <option value="4">Medium-High (4)</option>
            <option value="5">High (5)</option>
          </Select>
        </div>

        {goal && (
          <div className="form-group">
            <Select
              label="Status"
              name="status"
              value={formData.status || 'active'}
              onChange={handleChange}
            >
              <option value="active">Active</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="paused">Paused</option>
              <option value="cancelled">Cancelled</option>
            </Select>
          </div>
        )}
      </div>

      <div className="form-row">
        <div className="form-group full-width">
          <TextArea
            label="Description"
            name="description"
            value={formData.description || ''}
            onChange={handleChange}
            placeholder="Describe your goal and why it's important to you..."
            rows={3}
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <Input
            label="Target Value (Optional)"
            name="target_value"
            type="number"
            value={formData.target_value?.toString() || ''}
            onChange={handleChange}
            placeholder="e.g., 100000"
          />
        </div>

        <div className="form-group">
          <Input
            label="Target Unit (Optional)"
            name="target_unit"
            value={formData.target_unit || ''}
            onChange={handleChange}
            placeholder="e.g., dollars, countries, books"
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <Input
            label="Start Date (Optional)"
            name="start_date"
            type="date"
            value={formData.start_date || ''}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <Input
            label="Target End Date (Optional)"
            name="end_date"
            type="date"
            value={formData.end_date || ''}
            onChange={handleChange}
          />
        </div>
      </div>

      <div className="form-actions">
        <Button type="button" onClick={onCancel} variant="secondary" disabled={submitting}>
          Cancel
        </Button>
        <Button type="submit" variant="primary" disabled={submitting}>
          {submitting ? 'Saving...' : goal ? 'Update Goal' : 'Create Goal'}
        </Button>
      </div>
    </form>
  );
};

export default LifeGoalForm;
