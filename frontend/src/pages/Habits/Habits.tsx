import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Habit, HabitInsights } from '../../types/habit';
import { habitService, habitAnalyticsService } from '../../services/habitService';
import './Habits.css';

const Habits: React.FC = () => {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [insights, setInsights] = useState<HabitInsights | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showActiveOnly, setShowActiveOnly] = useState(true);

  useEffect(() => {
    fetchData();
  }, [showActiveOnly]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [habitsData, insightsData] = await Promise.all([
        habitService.getHabits(showActiveOnly),
        habitAnalyticsService.getUserInsights(),
      ]);

      setHabits(habitsData.items);
      setInsights(insightsData);
    } catch (err) {
      console.error('Error fetching habits:', err);
      setError('Failed to load habits. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">Loading habits...</div>
      </div>
    );
  }

  return (
    <div className="page-container habits-page">
      <div className="page-header">
        <h1>My Habits</h1>
        <p>Build and maintain positive daily habits that support your goals and well-being.</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {insights && (
        <div className="insights-summary">
          <div className="insights-header">
            <h3>Your Progress</h3>
          </div>
          <div className="insights-stats">
            <div className="insight-stat">
              <div className="stat-value">{insights.total_active_streaks}</div>
              <div className="stat-label">Active Streaks</div>
            </div>
            <div className="insight-stat">
              <div className="stat-value">{insights.average_streak_length}</div>
              <div className="stat-label">Avg Streak Length</div>
            </div>
            <div className="insight-stat">
              <div className="stat-value">{Math.round(insights.overall_completion_rate)}%</div>
              <div className="stat-label">Overall Completion</div>
            </div>
          </div>
          {insights.motivational_insights.length > 0 && (
            <div className="insights-messages">
              {insights.motivational_insights.map((message, idx) => (
                <p key={idx} className="insight-message">{message}</p>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="habits-controls">
        <button
          className={`filter-btn ${showActiveOnly ? 'active' : ''}`}
          onClick={() => setShowActiveOnly(!showActiveOnly)}
        >
          {showActiveOnly ? 'Show All' : 'Show Active Only'}
        </button>
      </div>

      {habits.length === 0 ? (
        <div className="empty-state">
          <p>No habits yet. Start building your positive habits today!</p>
        </div>
      ) : (
        <div className="habits-grid">
          {habits.map((habit) => (
            <div key={habit.id} className="habit-card">
              <div className="habit-header">
                <h3>{habit.name}</h3>
                {habit.is_active && <span className="active-badge">Active</span>}
              </div>
              {habit.description && <p className="habit-description">{habit.description}</p>}
              
              <div className="habit-stats">
                <div className="stat">
                  <span className="stat-icon">🔥</span>
                  <span className="stat-value">{habit.current_streak}</span>
                  <span className="stat-label">Current Streak</span>
                </div>
                <div className="stat">
                  <span className="stat-icon">🏆</span>
                  <span className="stat-value">{habit.longest_streak}</span>
                  <span className="stat-label">Longest Streak</span>
                </div>
                <div className="stat">
                  <span className="stat-icon">✅</span>
                  <span className="stat-value">{habit.total_completions}</span>
                  <span className="stat-label">Total</span>
                </div>
              </div>

              <div className="habit-actions">
                <Link to={`/habits/${habit.id}/analytics`} className="btn-analytics">
                  View Analytics
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Habits;
