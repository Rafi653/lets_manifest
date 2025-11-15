/**
 * MotivationalInsights component - Displays personalized motivational messages and insights
 */

import React from 'react';
import './MotivationalInsights.css';

interface MotivationalInsightsProps {
  message: string;
  insights?: string[];
}

const MotivationalInsights: React.FC<MotivationalInsightsProps> = ({ message, insights }) => {
  return (
    <div className="motivational-insights">
      <div className="main-message">
        <div className="message-icon">💪</div>
        <p className="message-text">{message}</p>
      </div>

      {insights && insights.length > 0 && (
        <div className="insights-list">
          <h5>Your Insights</h5>
          <ul>
            {insights.map((insight, index) => (
              <li key={index} className="insight-item">
                <span className="insight-bullet">✨</span>
                <span className="insight-text">{insight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default MotivationalInsights;
