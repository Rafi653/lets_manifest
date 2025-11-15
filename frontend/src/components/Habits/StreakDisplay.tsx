/**
 * StreakDisplay component - Shows current and longest streaks with visual indicators
 */

import React from 'react';
import type { StreakInfo } from '../../types/habit';
import './StreakDisplay.css';

interface StreakDisplayProps {
  streakInfo: StreakInfo;
  habitName: string;
}

const StreakDisplay: React.FC<StreakDisplayProps> = ({ streakInfo, habitName }) => {
  const getStreakEmoji = (streak: number): string => {
    if (streak === 0) return '🌱';
    if (streak < 7) return '🔥';
    if (streak < 30) return '🚀';
    if (streak < 100) return '⭐';
    return '🏆';
  };

  const getStreakDescription = (streak: number): string => {
    if (streak === 0) return 'Start your journey';
    if (streak < 7) return 'Building momentum';
    if (streak < 30) return 'Strong habit forming';
    if (streak < 100) return 'Incredible consistency';
    return 'Legendary streak';
  };

  return (
    <div className="streak-display">
      <div className="streak-header">
        <h3>{habitName}</h3>
        {streakInfo.is_active && (
          <span className="streak-badge active">Active</span>
        )}
      </div>

      <div className="streak-stats">
        <div className="streak-stat current">
          <div className="streak-icon">{getStreakEmoji(streakInfo.current_streak)}</div>
          <div className="streak-info">
            <div className="streak-number">{streakInfo.current_streak}</div>
            <div className="streak-label">Current Streak</div>
            <div className="streak-description">
              {getStreakDescription(streakInfo.current_streak)}
            </div>
          </div>
        </div>

        <div className="streak-stat longest">
          <div className="streak-icon">🏅</div>
          <div className="streak-info">
            <div className="streak-number">{streakInfo.longest_streak}</div>
            <div className="streak-label">Longest Streak</div>
            {streakInfo.current_streak === streakInfo.longest_streak && 
             streakInfo.current_streak > 0 && (
              <div className="streak-record">Personal Best!</div>
            )}
          </div>
        </div>
      </div>

      {streakInfo.last_completed_date && (
        <div className="streak-footer">
          <p className="last-completed">
            Last completed: {new Date(streakInfo.last_completed_date).toLocaleDateString()}
          </p>
          {streakInfo.streak_start_date && (
            <p className="streak-started">
              Current streak started: {new Date(streakInfo.streak_start_date).toLocaleDateString()}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default StreakDisplay;
