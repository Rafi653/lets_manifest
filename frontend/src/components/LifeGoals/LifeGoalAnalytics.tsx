import React, { useState, useEffect } from 'react';
import type { LifeGoalSummary, MilestoneStatistics, GoalsByLifeArea } from '../../types/goal';
import { lifeGoalService } from '../../services/lifeGoalService';
import './LifeGoalAnalytics.css';

const LifeGoalAnalytics: React.FC = () => {
  const [summary, setSummary] = useState<LifeGoalSummary | null>(null);
  const [milestoneStats, setMilestoneStats] = useState<MilestoneStatistics | null>(null);
  const [goalsByArea, setGoalsByArea] = useState<GoalsByLifeArea[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const [summaryData, milestoneData, byAreaData] = await Promise.all([
        lifeGoalService.getLifeGoalSummary(),
        lifeGoalService.getMilestoneStatistics(),
        lifeGoalService.getGoalsByLifeArea(),
      ]);

      setSummary(summaryData);
      setMilestoneStats(milestoneData);
      setGoalsByArea(byAreaData);
    } catch (err) {
      console.error('Failed to load analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="analytics-loading">Loading analytics...</div>;
  }

  return (
    <div className="life-goal-analytics">
      <h2>Life Goals Analytics</h2>

      {summary && (
        <div className="analytics-section">
          <h3>Overview</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-value">{summary.total_goals}</div>
              <div className="stat-label">Total Life Goals</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{summary.active_goals}</div>
              <div className="stat-label">Active Goals</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{summary.completed_goals}</div>
              <div className="stat-label">Completed</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{summary.cancelled_goals}</div>
              <div className="stat-label">Cancelled</div>
            </div>
            <div className="stat-card highlight">
              <div className="stat-value">{summary.completion_rate.toFixed(1)}%</div>
              <div className="stat-label">Completion Rate</div>
            </div>
            {summary.avg_days_to_complete && (
              <div className="stat-card highlight">
                <div className="stat-value">{summary.avg_days_to_complete}</div>
                <div className="stat-label">Avg. Days to Complete</div>
              </div>
            )}
          </div>
        </div>
      )}

      {milestoneStats && (
        <div className="analytics-section">
          <h3>Milestones Progress</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-value">{milestoneStats.total_milestones}</div>
              <div className="stat-label">Total Milestones</div>
            </div>
            <div className="stat-card success">
              <div className="stat-value">{milestoneStats.completed_milestones}</div>
              <div className="stat-label">Completed</div>
            </div>
            <div className="stat-card info">
              <div className="stat-value">{milestoneStats.in_progress_milestones}</div>
              <div className="stat-label">In Progress</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{milestoneStats.pending_milestones}</div>
              <div className="stat-label">Pending</div>
            </div>
            <div className="stat-card highlight">
              <div className="stat-value">{milestoneStats.completion_rate.toFixed(1)}%</div>
              <div className="stat-label">Completion Rate</div>
            </div>
          </div>
        </div>
      )}

      {goalsByArea.length > 0 && (
        <div className="analytics-section">
          <h3>Goals by Life Area</h3>
          <div className="life-areas-grid">
            {goalsByArea.map(area => (
              <div key={area.life_area} className="life-area-card">
                <div className="life-area-header">
                  <h4>{area.life_area.charAt(0).toUpperCase() + area.life_area.slice(1).replace('_', ' ')}</h4>
                  <span className="goal-count-badge">{area.goal_count}</span>
                </div>
                <div className="life-area-goals">
                  {area.goals.map(goal => (
                    <div key={goal.id} className="mini-goal-card">
                      <div className="mini-goal-title">{goal.title}</div>
                      <span className={`mini-goal-status status-${goal.status}`}>
                        {goal.status.replace('_', ' ')}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {summary && (
        <div className="analytics-section">
          <h3>Goals by Category</h3>
          <div className="category-bars">
            {Object.entries(summary.goals_by_category).map(([category, count]) => {
              const percentage = (count / summary.total_goals) * 100;
              return (
                <div key={category} className="category-bar">
                  <div className="category-label">
                    {category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')}
                  </div>
                  <div className="category-progress">
                    <div 
                      className="category-fill" 
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <div className="category-count">{count}</div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default LifeGoalAnalytics;
