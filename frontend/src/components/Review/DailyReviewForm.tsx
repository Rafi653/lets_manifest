/**
 * DailyReviewForm component for creating and editing daily reviews
 */

import React, { useState } from 'react';
import type { DailyReview, DailyReviewCreate, DailyReviewUpdate } from '../../types/dailyReview';
import Input from '../common/Input';
import TextArea from '../common/TextArea';
import Button from '../common/Button';
import './DailyReviewForm.css';

interface DailyReviewFormProps {
  review?: DailyReview;
  onSubmit: (data: DailyReviewCreate | DailyReviewUpdate) => Promise<void>;
  onCancel: () => void;
}

const DailyReviewForm: React.FC<DailyReviewFormProps> = ({ review, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    review_date: review?.review_date || new Date().toISOString().split('T')[0],
    mood_rating: review?.mood_rating?.toString() || '',
    energy_level: review?.energy_level?.toString() || '',
    productivity_rating: review?.productivity_rating?.toString() || '',
    sleep_hours: review?.sleep_hours?.toString() || '',
    sleep_quality: review?.sleep_quality?.toString() || '',
    water_intake_ml: review?.water_intake_ml?.toString() || '',
    screen_time_minutes: review?.screen_time_minutes?.toString() || '',
    steps: review?.steps?.toString() || '',
    accomplishments: review?.accomplishments || '',
    challenges: review?.challenges || '',
    lessons_learned: review?.lessons_learned || '',
    gratitude: review?.gratitude || '',
    tomorrow_intentions: review?.tomorrow_intentions || '',
    highlights: review?.highlights || '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
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

    if (!formData.review_date) {
      newErrors.review_date = 'Review date is required';
    }

    // Validate rating fields (1-10)
    const ratingFields = ['mood_rating', 'energy_level', 'productivity_rating', 'sleep_quality'];
    ratingFields.forEach((field) => {
      const value = formData[field as keyof typeof formData];
      if (value && (isNaN(Number(value)) || Number(value) < 1 || Number(value) > 10)) {
        newErrors[field] = 'Must be a number between 1 and 10';
      }
    });

    // Validate sleep hours (0-24)
    if (formData.sleep_hours) {
      const hours = Number(formData.sleep_hours);
      if (isNaN(hours) || hours < 0 || hours > 24) {
        newErrors.sleep_hours = 'Must be a number between 0 and 24';
      }
    }

    // Validate water intake
    if (formData.water_intake_ml) {
      const intake = Number(formData.water_intake_ml);
      if (isNaN(intake) || intake < 0) {
        newErrors.water_intake_ml = 'Must be a positive number';
      }
    }

    // Validate screen time
    if (formData.screen_time_minutes) {
      const screenTime = Number(formData.screen_time_minutes);
      if (isNaN(screenTime) || screenTime < 0) {
        newErrors.screen_time_minutes = 'Must be a positive number';
      }
    }

    // Validate steps
    if (formData.steps) {
      const stepCount = Number(formData.steps);
      if (isNaN(stepCount) || stepCount < 0) {
        newErrors.steps = 'Must be a positive number';
      }
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
      const submitData: DailyReviewCreate | DailyReviewUpdate = {
        mood_rating: formData.mood_rating ? Number(formData.mood_rating) : null,
        energy_level: formData.energy_level ? Number(formData.energy_level) : null,
        productivity_rating: formData.productivity_rating ? Number(formData.productivity_rating) : null,
        sleep_hours: formData.sleep_hours ? Number(formData.sleep_hours) : null,
        sleep_quality: formData.sleep_quality ? Number(formData.sleep_quality) : null,
        water_intake_ml: formData.water_intake_ml ? Number(formData.water_intake_ml) : null,
        screen_time_minutes: formData.screen_time_minutes ? Number(formData.screen_time_minutes) : null,
        steps: formData.steps ? Number(formData.steps) : null,
        accomplishments: formData.accomplishments.trim() || null,
        challenges: formData.challenges.trim() || null,
        lessons_learned: formData.lessons_learned.trim() || null,
        gratitude: formData.gratitude.trim() || null,
        tomorrow_intentions: formData.tomorrow_intentions.trim() || null,
        highlights: formData.highlights.trim() || null,
      };

      // Add review_date for create operations
      if (!review) {
        (submitData as DailyReviewCreate).review_date = formData.review_date;
      }

      await onSubmit(submitData);
    } catch (error) {
      console.error('Form submission error:', error);
      setErrors({ submit: 'Failed to save review. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="daily-review-form" onSubmit={handleSubmit}>
      <div className="form-section">
        <h3 className="section-title">Basic Information</h3>
        
        <Input
          label="Review Date"
          name="review_date"
          type="date"
          value={formData.review_date}
          onChange={handleChange}
          error={errors.review_date}
          required
          disabled={!!review}
        />
      </div>

      <div className="form-section">
        <h3 className="section-title">Daily Metrics</h3>
        
        <div className="form-row">
          <Input
            label="Mood Rating"
            name="mood_rating"
            type="number"
            min="1"
            max="10"
            value={formData.mood_rating}
            onChange={handleChange}
            error={errors.mood_rating}
            helperText="Rate your mood (1-10)"
          />

          <Input
            label="Energy Level"
            name="energy_level"
            type="number"
            min="1"
            max="10"
            value={formData.energy_level}
            onChange={handleChange}
            error={errors.energy_level}
            helperText="Rate your energy (1-10)"
          />

          <Input
            label="Productivity Rating"
            name="productivity_rating"
            type="number"
            min="1"
            max="10"
            value={formData.productivity_rating}
            onChange={handleChange}
            error={errors.productivity_rating}
            helperText="Rate productivity (1-10)"
          />
        </div>

        <div className="form-row">
          <Input
            label="Sleep Hours"
            name="sleep_hours"
            type="number"
            step="0.5"
            min="0"
            max="24"
            value={formData.sleep_hours}
            onChange={handleChange}
            error={errors.sleep_hours}
            helperText="Hours of sleep (0-24)"
          />

          <Input
            label="Sleep Quality"
            name="sleep_quality"
            type="number"
            min="1"
            max="10"
            value={formData.sleep_quality}
            onChange={handleChange}
            error={errors.sleep_quality}
            helperText="Rate sleep quality (1-10)"
          />

          <Input
            label="Water Intake (ml)"
            name="water_intake_ml"
            type="number"
            min="0"
            value={formData.water_intake_ml}
            onChange={handleChange}
            error={errors.water_intake_ml}
            helperText="Water consumed in ml"
          />
        </div>

        <div className="form-row">
          <Input
            label="Screen Time (minutes)"
            name="screen_time_minutes"
            type="number"
            min="0"
            value={formData.screen_time_minutes}
            onChange={handleChange}
            error={errors.screen_time_minutes}
            helperText="Total screen time in minutes"
          />

          <Input
            label="Steps"
            name="steps"
            type="number"
            min="0"
            value={formData.steps}
            onChange={handleChange}
            error={errors.steps}
            helperText="Total steps walked today"
          />
        </div>
      </div>

      <div className="form-section">
        <h3 className="section-title">Reflections</h3>

        <TextArea
          label="Accomplishments"
          name="accomplishments"
          value={formData.accomplishments}
          onChange={handleChange}
          error={errors.accomplishments}
          placeholder="What did you accomplish today?"
          rows={3}
        />

        <TextArea
          label="Challenges"
          name="challenges"
          value={formData.challenges}
          onChange={handleChange}
          error={errors.challenges}
          placeholder="What challenges did you face?"
          rows={3}
        />

        <TextArea
          label="Lessons Learned"
          name="lessons_learned"
          value={formData.lessons_learned}
          onChange={handleChange}
          error={errors.lessons_learned}
          placeholder="What did you learn today?"
          rows={3}
        />

        <TextArea
          label="Gratitude"
          name="gratitude"
          value={formData.gratitude}
          onChange={handleChange}
          error={errors.gratitude}
          placeholder="What are you grateful for?"
          rows={3}
        />

        <TextArea
          label="Tomorrow's Intentions"
          name="tomorrow_intentions"
          value={formData.tomorrow_intentions}
          onChange={handleChange}
          error={errors.tomorrow_intentions}
          placeholder="What do you intend to do tomorrow?"
          rows={3}
        />

        <TextArea
          label="Highlights"
          name="highlights"
          value={formData.highlights}
          onChange={handleChange}
          error={errors.highlights}
          placeholder="What were the highlights of your day?"
          rows={3}
        />
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
          {review ? 'Update Review' : 'Create Review'}
        </Button>
      </div>
    </form>
  );
};

export default DailyReviewForm;
