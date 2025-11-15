/**
 * GoalForm component for creating and editing goals
 */

import React, { useState } from 'react';
import type { Goal, GoalCreate, GoalUpdate } from '../../types/goal';
import Input from '../common/Input';
import Select from '../common/Select';
import TextArea from '../common/TextArea';
import Button from '../common/Button';
import './GoalForm.css';

interface GoalFormProps {
  goal?: Goal;
  onSubmit: (data: GoalCreate | GoalUpdate) => Promise<void>;
  onCancel: () => void;
}

const GoalForm: React.FC<GoalFormProps> = ({ goal, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: goal?.title || '',
    description: goal?.description || '',
    goal_type: goal?.goal_type || '',
    category: goal?.category || '',
    target_value: goal?.target_value?.toString() || '',
    target_unit: goal?.target_unit || '',
    start_date: goal?.start_date || new Date().toISOString().split('T')[0],
    end_date: goal?.end_date || '',
    priority: goal?.priority?.toString() || '0',
    status: goal?.status || 'active',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const goalTypeOptions = [
    { value: 'daily', label: 'Daily' },
    { value: 'weekly', label: 'Weekly' },
    { value: 'monthly', label: 'Monthly' },
    { value: 'yearly', label: 'Yearly' },
  ];

  const statusOptions = [
    { value: 'active', label: 'Active' },
    { value: 'completed', label: 'Completed' },
    { value: 'paused', label: 'Paused' },
    { value: 'cancelled', label: 'Cancelled' },
  ];

  const priorityOptions = [
    { value: '0', label: 'None' },
    { value: '1', label: 'Low' },
    { value: '2', label: 'Medium-Low' },
    { value: '3', label: 'Medium' },
    { value: '4', label: 'Medium-High' },
    { value: '5', label: 'High' },
  ];

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 255) {
      newErrors.title = 'Title must be less than 255 characters';
    }

    if (!formData.goal_type) {
      newErrors.goal_type = 'Goal type is required';
    }

    if (!formData.start_date) {
      newErrors.start_date = 'Start date is required';
    }

    if (!formData.end_date) {
      newErrors.end_date = 'End date is required';
    }

    if (formData.start_date && formData.end_date) {
      const start = new Date(formData.start_date);
      const end = new Date(formData.end_date);
      if (end < start) {
        newErrors.end_date = 'End date must be after start date';
      }
    }

    if (formData.target_value && isNaN(Number(formData.target_value))) {
      newErrors.target_value = 'Target value must be a number';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setLoading(true);

    try {
      const submitData: GoalCreate | GoalUpdate = {
        title: formData.title.trim(),
        description: formData.description.trim() || null,
        goal_type: formData.goal_type as 'daily' | 'weekly' | 'monthly' | 'yearly',
        category: formData.category.trim() || null,
        target_value: formData.target_value ? Number(formData.target_value) : null,
        target_unit: formData.target_unit.trim() || null,
        start_date: formData.start_date,
        end_date: formData.end_date,
        priority: Number(formData.priority),
      };

      // Add status for updates
      if (goal) {
        (submitData as GoalUpdate).status = formData.status as
          | 'active'
          | 'completed'
          | 'cancelled'
          | 'paused';
      }

      await onSubmit(submitData);
    } catch (error) {
      console.error('Form submission error:', error);
      setErrors({ submit: 'Failed to save goal. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="goal-form" onSubmit={handleSubmit}>
      <Input
        label="Title"
        name="title"
        value={formData.title}
        onChange={handleChange}
        error={errors.title}
        placeholder="Enter your goal title"
        required
      />

      <TextArea
        label="Description"
        name="description"
        value={formData.description}
        onChange={handleChange}
        error={errors.description}
        placeholder="Describe your goal (optional)"
      />

      <div className="form-row">
        <Select
          label="Goal Type"
          name="goal_type"
          value={formData.goal_type}
          onChange={handleChange}
          options={goalTypeOptions}
          error={errors.goal_type}
          required
        />

        <Input
          label="Category"
          name="category"
          value={formData.category}
          onChange={handleChange}
          error={errors.category}
          placeholder="e.g., Health, Career, Personal"
        />
      </div>

      <div className="form-row">
        <Input
          label="Target Value"
          name="target_value"
          type="number"
          step="0.01"
          value={formData.target_value}
          onChange={handleChange}
          error={errors.target_value}
          placeholder="e.g., 10"
        />

        <Input
          label="Target Unit"
          name="target_unit"
          value={formData.target_unit}
          onChange={handleChange}
          error={errors.target_unit}
          placeholder="e.g., kg, hours, pages"
        />
      </div>

      <div className="form-row">
        <Input
          label="Start Date"
          name="start_date"
          type="date"
          value={formData.start_date}
          onChange={handleChange}
          error={errors.start_date}
          required
        />

        <Input
          label="End Date"
          name="end_date"
          type="date"
          value={formData.end_date}
          onChange={handleChange}
          error={errors.end_date}
          required
        />
      </div>

      <div className="form-row">
        <Select
          label="Priority"
          name="priority"
          value={formData.priority}
          onChange={handleChange}
          options={priorityOptions}
          error={errors.priority}
        />

        {goal && (
          <Select
            label="Status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            options={statusOptions}
            error={errors.status}
          />
        )}
      </div>

      {errors.submit && (
        <div className="form-error" role="alert">
          {errors.submit}
        </div>
      )}

      <div className="form-actions">
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" variant="primary" loading={loading}>
          {goal ? 'Update Goal' : 'Create Goal'}
        </Button>
      </div>
    </form>
  );
};

export default GoalForm;
