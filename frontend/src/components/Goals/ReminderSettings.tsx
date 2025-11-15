/**
 * ReminderSettings component for goal forms
 * Allows users to set reminder preferences for goals
 */

import React from 'react';

export interface ReminderSettingsProps {
  reminderEnabled: boolean;
  reminderTime: string;
  reminderDaysBefore: number;
  onReminderEnabledChange: (enabled: boolean) => void;
  onReminderTimeChange: (time: string) => void;
  onReminderDaysBeforeChange: (days: number) => void;
}

export const ReminderSettings: React.FC<ReminderSettingsProps> = ({
  reminderEnabled,
  reminderTime,
  reminderDaysBefore,
  onReminderEnabledChange,
  onReminderTimeChange,
  onReminderDaysBeforeChange,
}) => {
  return (
    <div className="reminder-settings">
      <h3>Reminder Settings</h3>
      
      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={reminderEnabled}
            onChange={(e) => onReminderEnabledChange(e.target.checked)}
          />
          <span> Enable reminders for this goal</span>
        </label>
      </div>

      {reminderEnabled && (
        <>
          <div className="form-group">
            <label htmlFor="reminderTime">
              Reminder Time
              <input
                id="reminderTime"
                type="time"
                value={reminderTime || '09:00'}
                onChange={(e) => onReminderTimeChange(e.target.value)}
                className="form-control"
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="reminderDaysBefore">
              Days Before Deadline
              <input
                id="reminderDaysBefore"
                type="number"
                min="0"
                max="365"
                value={reminderDaysBefore || 1}
                onChange={(e) =>
                  onReminderDaysBeforeChange(parseInt(e.target.value, 10))
                }
                className="form-control"
              />
            </label>
            <small className="form-text">
              Receive a reminder this many days before your goal deadline
            </small>
          </div>
        </>
      )}

      <style>{`
        .reminder-settings {
          border: 1px solid #ddd;
          border-radius: 4px;
          padding: 16px;
          margin: 16px 0;
        }

        .reminder-settings h3 {
          margin-top: 0;
          font-size: 18px;
          font-weight: 600;
          margin-bottom: 16px;
        }

        .form-group {
          margin-bottom: 16px;
        }

        .form-group label {
          display: block;
          font-weight: 500;
          margin-bottom: 8px;
        }

        .form-control {
          width: 100%;
          padding: 8px 12px;
          border: 1px solid #ccc;
          border-radius: 4px;
          font-size: 14px;
        }

        .form-control:focus {
          outline: none;
          border-color: #4CAF50;
          box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }

        .form-text {
          display: block;
          margin-top: 4px;
          font-size: 12px;
          color: #666;
        }

        .form-group label input[type="checkbox"] {
          width: auto;
          margin-right: 8px;
        }
      `}</style>
    </div>
  );
};
