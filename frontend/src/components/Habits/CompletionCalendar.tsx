/**
 * CompletionCalendar component - Calendar view of habit completions
 */

import React from 'react';
import type { DailyCompletionData } from '../../types/habit';
import './CompletionCalendar.css';

interface CompletionCalendarProps {
  dailyData: DailyCompletionData[];
  habitName: string;
}

const CompletionCalendar: React.FC<CompletionCalendarProps> = ({ dailyData, habitName }) => {
  const getDayColor = (completed: boolean): string => {
    return completed ? '#10b981' : '#e5e7eb';
  };

  const getDayLabel = (dateStr: string): string => {
    const date = new Date(dateStr);
    return date.getDate().toString();
  };

  const getMonthGroups = (data: DailyCompletionData[]): Map<string, DailyCompletionData[]> => {
    const groups = new Map<string, DailyCompletionData[]>();
    
    data.forEach((day) => {
      const date = new Date(day.date);
      const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
      
      if (!groups.has(monthKey)) {
        groups.set(monthKey, []);
      }
      groups.get(monthKey)!.push(day);
    });

    return groups;
  };

  const getMonthName = (monthKey: string): string => {
    const [year, month] = monthKey.split('-');
    const date = new Date(parseInt(year), parseInt(month) - 1);
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  };

  const monthGroups = getMonthGroups(dailyData);

  return (
    <div className="completion-calendar">
      <h4>Completion Calendar - {habitName}</h4>
      
      {Array.from(monthGroups.entries()).reverse().map(([monthKey, days]) => (
        <div key={monthKey} className="calendar-month">
          <h5 className="month-label">{getMonthName(monthKey)}</h5>
          
          <div className="calendar-grid">
            {days.map((day) => (
              <div
                key={day.date}
                className={`calendar-day ${day.completed ? 'completed' : 'missed'}`}
                style={{ backgroundColor: getDayColor(day.completed) }}
                title={`${day.date}${day.completed ? ' - Completed' : ' - Missed'}${day.mood ? ` (${day.mood})` : ''}`}
              >
                <span className="day-number">{getDayLabel(day.date)}</span>
                {day.completed && <span className="check-mark">✓</span>}
              </div>
            ))}
          </div>
        </div>
      ))}

      <div className="calendar-legend">
        <div className="legend-item">
          <div className="legend-box completed"></div>
          <span>Completed</span>
        </div>
        <div className="legend-item">
          <div className="legend-box missed"></div>
          <span>Missed</span>
        </div>
      </div>
    </div>
  );
};

export default CompletionCalendar;
