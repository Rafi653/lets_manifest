import React, { useState, useEffect } from 'react';
import type { Food as FoodType, CreateFoodRequest, UpdateFoodRequest } from '../../types/food';
import { foodService } from '../../services/foodService';
import FoodForm from '../../components/Food/FoodForm';
import FoodList from '../../components/Food/FoodList';
import Button from '../../components/common/Button';
import Select from '../../components/common/Select';
import Input from '../../components/common/Input';
import './Food.css';

const Food: React.FC = () => {
  const [foods, setFoods] = useState<FoodType[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingFood, setEditingFood] = useState<FoodType | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [mealTypeFilter, setMealTypeFilter] = useState<string>('');
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  useEffect(() => {
    loadFoods();
  }, [mealTypeFilter, startDate, endDate, page]);

  const loadFoods = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await foodService.getFoods(
        mealTypeFilter || undefined,
        startDate || undefined,
        endDate || undefined,
        page,
        20
      );
      setFoods(data.items);
      setTotalPages(data.total_pages);
    } catch (err) {
      console.error('Failed to load foods:', err);
      setError('Failed to load food entries. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFood = async (data: CreateFoodRequest | UpdateFoodRequest) => {
    try {
      await foodService.createFood(data as CreateFoodRequest);
      await loadFoods();
      setShowForm(false);
    } catch (err) {
      console.error('Failed to create food:', err);
      throw err;
    }
  };

  const handleUpdateFood = async (data: CreateFoodRequest | UpdateFoodRequest) => {
    if (!editingFood) return;

    try {
      await foodService.updateFood(editingFood.id, data as UpdateFoodRequest);
      await loadFoods();
      setEditingFood(undefined);
      setShowForm(false);
    } catch (err) {
      console.error('Failed to update food:', err);
      throw err;
    }
  };

  const handleDeleteFood = async (foodId: string) => {
    if (!window.confirm('Are you sure you want to delete this food entry?')) {
      return;
    }

    try {
      await foodService.deleteFood(foodId);
      await loadFoods();
    } catch (err) {
      console.error('Failed to delete food:', err);
      setError('Failed to delete food entry. Please try again.');
    }
  };

  const handleEditFood = (food: FoodType) => {
    setEditingFood(food);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingFood(undefined);
  };

  const handleNewFood = () => {
    setEditingFood(undefined);
    setShowForm(true);
  };

  const clearFilters = () => {
    setMealTypeFilter('');
    setStartDate('');
    setEndDate('');
    setPage(1);
  };

  // Calculate nutrition totals
  const totals = foods.reduce(
    (acc, food) => ({
      calories: acc.calories + (food.calories || 0),
      protein: acc.protein + (food.protein_grams || 0),
      carbs: acc.carbs + (food.carbs_grams || 0),
      fats: acc.fats + (food.fats_grams || 0),
    }),
    { calories: 0, protein: 0, carbs: 0, fats: 0 }
  );

  return (
    <div className="page-container food-page">
      <div className="page-header">
        <div>
          <h1>Food Tracking</h1>
          <p>Monitor your nutrition and eating habits to maintain a healthy lifestyle.</p>
        </div>
        {!showForm && (
          <Button onClick={handleNewFood} variant="primary">
            + Log Food
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
          <h2>{editingFood ? 'Edit Food Entry' : 'Log New Food'}</h2>
          <FoodForm
            food={editingFood}
            onSubmit={editingFood ? handleUpdateFood : handleCreateFood}
            onCancel={handleCancelForm}
          />
        </div>
      )}

      {!showForm && (
        <>
          {foods.length > 0 && (
            <div className="nutrition-summary">
              <h3>Nutrition Summary</h3>
              <div className="summary-stats">
                <div className="summary-stat">
                  <div className="stat-value">{Math.round(totals.calories)}</div>
                  <div className="stat-label">Calories</div>
                </div>
                <div className="summary-stat">
                  <div className="stat-value">{Math.round(totals.protein)}g</div>
                  <div className="stat-label">Protein</div>
                </div>
                <div className="summary-stat">
                  <div className="stat-value">{Math.round(totals.carbs)}g</div>
                  <div className="stat-label">Carbs</div>
                </div>
                <div className="summary-stat">
                  <div className="stat-value">{Math.round(totals.fats)}g</div>
                  <div className="stat-label">Fats</div>
                </div>
              </div>
            </div>
          )}

          <div className="filters-container">
            <div className="filters">
              <Select
                label="Meal Type"
                value={mealTypeFilter}
                onChange={(e) => {
                  setMealTypeFilter(e.target.value);
                  setPage(1);
                }}
              >
                <option value="">All Meals</option>
                <option value="breakfast">Breakfast</option>
                <option value="lunch">Lunch</option>
                <option value="dinner">Dinner</option>
                <option value="snack">Snack</option>
              </Select>

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

          <FoodList
            foods={foods}
            onEdit={handleEditFood}
            onDelete={handleDeleteFood}
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

export default Food;
