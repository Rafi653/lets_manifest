/**
 * HabitAnalyticsDashboard component - Comprehensive view of habit analytics
 */

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import type { HabitAnalytics, ProgressTrends } from '../../types/habit';
import { habitAnalyticsService } from '../../services/habitService';
import StreakDisplay from './StreakDisplay';
import CompletionStatsComponent from './CompletionStats';
import CompletionCalendar from './CompletionCalendar';
import MotivationalInsights from './MotivationalInsights';
import './HabitAnalyticsDashboard.css';

const HabitAnalyticsDashboard: React.FC = () => {
  const { habitId } = useParams<{ habitId: string }>();
  const [analytics, setAnalytics] = useState<HabitAnalytics | null>(null);
  const [progressTrends, setProgressTrends] = useState<ProgressTrends | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDays, setSelectedDays] = useState(90);

  useEffect(() => {
    if (!habitId) return;

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [analyticsData, trendsData] = await Promise.all([
          habitAnalyticsService.getAnalytics(habitId),
          habitAnalyticsService.getProgressTrends(habitId, selectedDays),
        ]);

        setAnalytics(analyticsData);
        setProgressTrends(trendsData);
      } catch (err) {
        console.error('Error fetching analytics:', err);
        setError('Failed to load habit analytics. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [habitId, selectedDays]);

  const handleDaysChange = (days: number) => {
    setSelectedDays(days);
  };

  if (loading) {
    return (
      <div className="analytics-dashboard loading">
        <div className="loading-spinner">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics-dashboard error">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  if (!analytics || !progressTrends) {
    return (
      <div className="analytics-dashboard error">
        <div className="error-message">No analytics data available.</div>
      </div>
    );
  }

  return (
    <div className="analytics-dashboard">
      <div className="dashboard-header">
        <h2>Habit Analytics</h2>
        <div className="time-period-selector">
          <button
            className={selectedDays === 30 ? 'active' : ''}
            onClick={() => handleDaysChange(30)}
          >
            30 Days
          </button>
          <button
            className={selectedDays === 90 ? 'active' : ''}
            onClick={() => handleDaysChange(90)}
          >
            90 Days
          </button>
          <button
            className={selectedDays === 180 ? 'active' : ''}
            onClick={() => handleDaysChange(180)}
          >
            6 Months
          </button>
          <button
            className={selectedDays === 365 ? 'active' : ''}
            onClick={() => handleDaysChange(365)}
          >
            1 Year
          </button>
        </div>
      </div>

      <MotivationalInsights message={analytics.motivational_message} />

      <StreakDisplay
        streakInfo={analytics.streak_info}
        habitName={analytics.habit_name}
      />

      <CompletionStatsComponent
        stats={analytics.completion_stats}
        confidenceLevel={analytics.confidence_level}
      />

      <CompletionCalendar
        dailyData={progressTrends.daily_data}
        habitName={analytics.habit_name}
      />

      {progressTrends.overall_trend !== 'no_data' && (
        <div className="trend-indicator">
          <h4>Overall Trend</h4>
          <div className={`trend-badge ${progressTrends.overall_trend}`}>
            {progressTrends.overall_trend === 'improving' && '📈 Improving'}
            {progressTrends.overall_trend === 'stable' && '➡️ Stable'}
            {progressTrends.overall_trend === 'declining' && '📉 Needs Attention'}
          </div>
        </div>
      )}
    </div>
  );
};

export default HabitAnalyticsDashboard;
