import React from 'react';
import type { Food } from '../../types/food';
import Button from '../common/Button';
import './FoodList.css';

interface FoodListProps {
  foods: Food[];
  onEdit: (food: Food) => void;
  onDelete: (foodId: string) => void;
  loading?: boolean;
}

const FoodList: React.FC<FoodListProps> = ({ foods, onEdit, onDelete, loading }) => {
  if (loading) {
    return <div className="loading">Loading food entries...</div>;
  }

  if (foods.length === 0) {
    return (
      <div className="empty-state">
        <p>No food entries yet. Start tracking your meals!</p>
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

  const getMealTypeColor = (mealType: string) => {
    const colors: Record<string, string> = {
      breakfast: '#ff9800',
      lunch: '#4caf50',
      dinner: '#2196f3',
      snack: '#9c27b0',
    };
    return colors[mealType] || '#757575';
  };

  return (
    <div className="food-list">
      <table className="food-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Meal</th>
            <th>Food</th>
            <th>Portion</th>
            <th>Calories</th>
            <th>Protein</th>
            <th>Carbs</th>
            <th>Fats</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {foods.map((food) => (
            <tr key={food.id}>
              <td>
                <div className="date-cell">
                  <div>{formatDate(food.meal_date)}</div>
                  {food.meal_time && (
                    <div className="time-text">{formatTime(food.meal_time)}</div>
                  )}
                </div>
              </td>
              <td>
                <span
                  className="meal-type-badge"
                  style={{ backgroundColor: getMealTypeColor(food.meal_type) }}
                >
                  {food.meal_type}
                </span>
              </td>
              <td>
                <div className="food-name">
                  {food.is_favorite && <span className="favorite-icon">⭐</span>}
                  {food.food_name}
                </div>
              </td>
              <td>{food.portion_size || '-'}</td>
              <td>{food.calories ? Math.round(food.calories) : '-'}</td>
              <td>{food.protein_grams ? `${food.protein_grams}g` : '-'}</td>
              <td>{food.carbs_grams ? `${food.carbs_grams}g` : '-'}</td>
              <td>{food.fats_grams ? `${food.fats_grams}g` : '-'}</td>
              <td>
                <div className="action-buttons">
                  <Button
                    variant="secondary"
                    onClick={() => onEdit(food)}
                  >
                    Edit
                  </Button>
                  <Button
                    variant="danger"
                    onClick={() => onDelete(food.id)}
                  >
                    Delete
                  </Button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FoodList;
