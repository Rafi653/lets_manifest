import React, { useState } from 'react';
import type { Food, CreateFoodRequest, UpdateFoodRequest } from '../../types/food';
import Button from '../common/Button';
import Input from '../common/Input';
import Select from '../common/Select';
import TextArea from '../common/TextArea';
import './FoodForm.css';

interface FoodFormProps {
  food?: Food;
  onSubmit: (data: CreateFoodRequest | UpdateFoodRequest) => Promise<void>;
  onCancel: () => void;
}

const FoodForm: React.FC<FoodFormProps> = ({ food, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState<CreateFoodRequest>({
    meal_date: food?.meal_date || new Date().toISOString().split('T')[0],
    meal_time: food?.meal_time || '',
    meal_type: food?.meal_type || 'breakfast',
    food_name: food?.food_name || '',
    portion_size: food?.portion_size || '',
    calories: food?.calories || undefined,
    protein_grams: food?.protein_grams || undefined,
    carbs_grams: food?.carbs_grams || undefined,
    fats_grams: food?.fats_grams || undefined,
    fiber_grams: food?.fiber_grams || undefined,
    sugar_grams: food?.sugar_grams || undefined,
    sodium_mg: food?.sodium_mg || undefined,
    notes: food?.notes || '',
    is_favorite: food?.is_favorite || false,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else if (type === 'number') {
      const numValue = value === '' ? undefined : Number(value);
      setFormData((prev) => ({ ...prev, [name]: numValue }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await onSubmit(formData);
    } catch (err) {
      console.error('Error submitting food entry:', err);
      setError('Failed to save food entry. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="food-form" onSubmit={handleSubmit}>
      {error && <div className="error-message">{error}</div>}

      <div className="form-row">
        <Input
          label="Date *"
          type="date"
          name="meal_date"
          value={formData.meal_date}
          onChange={handleChange}
          required
        />

        <Input
          label="Time"
          type="time"
          name="meal_time"
          value={formData.meal_time}
          onChange={handleChange}
        />

        <Select
          label="Meal Type *"
          name="meal_type"
          value={formData.meal_type}
          onChange={handleChange}
          required
        >
          <option value="breakfast">Breakfast</option>
          <option value="lunch">Lunch</option>
          <option value="dinner">Dinner</option>
          <option value="snack">Snack</option>
        </Select>
      </div>

      <div className="form-row">
        <Input
          label="Food Name *"
          type="text"
          name="food_name"
          value={formData.food_name}
          onChange={handleChange}
          placeholder="e.g., Grilled chicken breast"
          required
        />

        <Input
          label="Portion Size"
          type="text"
          name="portion_size"
          value={formData.portion_size || ''}
          onChange={handleChange}
          placeholder="e.g., 6 oz, 1 cup"
        />
      </div>

      <div className="form-section">
        <h3>Nutrition Information (Optional)</h3>
        <div className="form-row">
          <Input
            label="Calories"
            type="number"
            name="calories"
            value={formData.calories || ''}
            onChange={handleChange}
            min="0"
            step="0.01"
          />

          <Input
            label="Protein (g)"
            type="number"
            name="protein_grams"
            value={formData.protein_grams || ''}
            onChange={handleChange}
            min="0"
            step="0.01"
          />

          <Input
            label="Carbs (g)"
            type="number"
            name="carbs_grams"
            value={formData.carbs_grams || ''}
            onChange={handleChange}
            min="0"
            step="0.01"
          />

          <Input
            label="Fats (g)"
            type="number"
            name="fats_grams"
            value={formData.fats_grams || ''}
            onChange={handleChange}
            min="0"
            step="0.01"
          />
        </div>

        <div className="form-row">
          <Input
            label="Fiber (g)"
            type="number"
            name="fiber_grams"
            value={formData.fiber_grams || ''}
            onChange={handleChange}
            min="0"
            step="0.01"
          />

          <Input
            label="Sugar (g)"
            type="number"
            name="sugar_grams"
            value={formData.sugar_grams || ''}
            onChange={handleChange}
            min="0"
            step="0.01"
          />

          <Input
            label="Sodium (mg)"
            type="number"
            name="sodium_mg"
            value={formData.sodium_mg || ''}
            onChange={handleChange}
            min="0"
            step="0.01"
          />
        </div>
      </div>

      <TextArea
        label="Notes"
        name="notes"
        value={formData.notes || ''}
        onChange={handleChange}
        placeholder="Any additional notes about this meal..."
        rows={3}
      />

      <div className="form-checkbox">
        <label>
          <input
            type="checkbox"
            name="is_favorite"
            checked={formData.is_favorite}
            onChange={handleChange}
          />
          <span>Mark as favorite</span>
        </label>
      </div>

      <div className="form-actions">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={loading}>
          Cancel
        </Button>
        <Button type="submit" variant="primary" disabled={loading}>
          {loading ? 'Saving...' : food ? 'Update' : 'Create'} Food Entry
        </Button>
      </div>
    </form>
  );
};

export default FoodForm;
