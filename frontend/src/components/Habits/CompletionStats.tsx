/**
 * CompletionStats component - Shows completion statistics and confidence level
 */

import React from 'react';
import type { CompletionStats as CompletionStatsType } from '../../types/habit';
import './CompletionStats.css';

interface CompletionStatsProps {
  stats: CompletionStatsType;
  confidenceLevel: number;
}

const CompletionStatsComponent: React.FC<CompletionStatsProps> = ({ stats, confidenceLevel }) => {
  const getConfidenceColor = (level: number): string => {
    if (level >= 80) return '#10b981';
    if (level >= 60) return '#f59e0b';
    if (level >= 40) return '#f97316';
    return '#ef4444';
  };

  const getConfidenceLabel = (level: number): string => {
    if (level >= 80) return 'Excellent';
    if (level >= 60) return 'Good';
    if (level >= 40) return 'Building';
    return 'Starting';
  };

  const formatPercentage = (value: number): string => {
    return `${Math.round(value)}%`;
  };

  return (
    <div className="completion-stats">
      <h4>Completion Statistics</h4>

      <div className="confidence-meter">
        <div className="confidence-header">
          <span className="confidence-label">Confidence Level</span>
          <span className="confidence-value" style={{ color: getConfidenceColor(confidenceLevel) }}>
            {confidenceLevel}% - {getConfidenceLabel(confidenceLevel)}
          </span>
        </div>
        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{
              width: `${confidenceLevel}%`,
              backgroundColor: getConfidenceColor(confidenceLevel),
            }}
          />
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <div className="stat-value">{stats.total_completions}</div>
            <div className="stat-label">Total Completions</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <div className="stat-value">{formatPercentage(stats.completion_rate)}</div>
            <div className="stat-label">Completion Rate</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <div className="stat-value">{stats.total_days_tracked}</div>
            <div className="stat-label">Days Tracked</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📆</div>
          <div className="stat-content">
            <div className="stat-value">{stats.current_month_completions}</div>
            <div className="stat-label">This Month</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🗓️</div>
          <div className="stat-content">
            <div className="stat-value">{stats.current_week_completions}</div>
            <div className="stat-label">This Week</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompletionStatsComponent;
