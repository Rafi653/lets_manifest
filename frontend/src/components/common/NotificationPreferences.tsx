/**
 * NotificationPreferences component
 * Allows users to manage their notification settings
 */

import React, { useState, useEffect } from 'react';
import { notificationService } from '../../services/notificationService';
import type {
  NotificationSettings,
  NotificationSettingsUpdate,
} from '../../types/notification';

export const NotificationPreferences: React.FC = () => {
  const [settings, setSettings] = useState<NotificationSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const data = await notificationService.getSettings();
      setSettings(data);
      setError(null);
    } catch (err) {
      setError('Failed to load notification settings');
      console.error('Failed to fetch settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!settings) return;

    try {
      setSaving(true);
      setError(null);
      setSuccessMessage(null);

      const updateData: NotificationSettingsUpdate = {
        email_enabled: settings.email_enabled,
        email_reminders: settings.email_reminders,
        email_goal_updates: settings.email_goal_updates,
        browser_enabled: settings.browser_enabled,
        browser_reminders: settings.browser_reminders,
        default_reminder_time: settings.default_reminder_time,
        reminder_before_hours: settings.reminder_before_hours,
      };

      const updated = await notificationService.updateSettings(updateData);
      setSettings(updated);
      setSuccessMessage('Settings saved successfully!');

      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError('Failed to save settings');
      console.error('Failed to save settings:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleBrowserPermission = async () => {
    try {
      const permission = await notificationService.requestPermission();
      if (permission === 'granted') {
        setSettings((prev) =>
          prev ? { ...prev, browser_enabled: true } : null
        );
        setSuccessMessage('Browser notifications enabled!');
      } else {
        setError('Browser notification permission denied');
      }
    } catch (err) {
      setError('Failed to request notification permission');
      console.error('Failed to request permission:', err);
    }
  };

  if (loading) {
    return <div className="preferences-container">Loading settings...</div>;
  }

  if (!settings) {
    return (
      <div className="preferences-container">
        <div className="error-message">Failed to load settings</div>
      </div>
    );
  }

  return (
    <div className="preferences-container">
      <h2>Notification Preferences</h2>

      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      <div className="settings-section">
        <h3>Email Notifications</h3>
        
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={settings.email_enabled}
            onChange={(e) =>
              setSettings({ ...settings, email_enabled: e.target.checked })
            }
          />
          <span>Enable email notifications</span>
        </label>

        {settings.email_enabled && (
          <>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.email_reminders}
                onChange={(e) =>
                  setSettings({ ...settings, email_reminders: e.target.checked })
                }
              />
              <span>Send email reminders</span>
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.email_goal_updates}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    email_goal_updates: e.target.checked,
                  })
                }
              />
              <span>Send goal update notifications</span>
            </label>
          </>
        )}
      </div>

      <div className="settings-section">
        <h3>Browser Notifications</h3>
        
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={settings.browser_enabled}
            onChange={(e) => {
              if (e.target.checked) {
                handleBrowserPermission();
              } else {
                setSettings({ ...settings, browser_enabled: false });
              }
            }}
          />
          <span>Enable browser notifications</span>
        </label>

        {settings.browser_enabled && (
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={settings.browser_reminders}
              onChange={(e) =>
                setSettings({ ...settings, browser_reminders: e.target.checked })
              }
            />
            <span>Show browser reminders</span>
          </label>
        )}
      </div>

      <div className="settings-section">
        <h3>Default Reminder Settings</h3>

        <div className="form-group">
          <label htmlFor="defaultTime">
            Default Reminder Time
            <input
              id="defaultTime"
              type="time"
              value={settings.default_reminder_time}
              onChange={(e) =>
                setSettings({
                  ...settings,
                  default_reminder_time: e.target.value,
                })
              }
              className="form-control"
            />
          </label>
        </div>

        <div className="form-group">
          <label htmlFor="reminderHours">
            Default Hours Before Deadline
            <input
              id="reminderHours"
              type="number"
              min="1"
              max="720"
              value={settings.reminder_before_hours}
              onChange={(e) =>
                setSettings({
                  ...settings,
                  reminder_before_hours: e.target.value,
                })
              }
              className="form-control"
            />
          </label>
        </div>
      </div>

      <div className="actions">
        <button
          onClick={handleSave}
          disabled={saving}
          className="btn-primary"
        >
          {saving ? 'Saving...' : 'Save Preferences'}
        </button>
      </div>

      <style>{`
        .preferences-container {
          max-width: 600px;
          margin: 0 auto;
          padding: 20px;
        }

        .preferences-container h2 {
          margin-top: 0;
          margin-bottom: 24px;
          font-size: 24px;
        }

        .settings-section {
          margin-bottom: 32px;
          padding-bottom: 24px;
          border-bottom: 1px solid #e0e0e0;
        }

        .settings-section:last-of-type {
          border-bottom: none;
        }

        .settings-section h3 {
          margin-top: 0;
          margin-bottom: 16px;
          font-size: 18px;
          font-weight: 600;
        }

        .checkbox-label {
          display: flex;
          align-items: center;
          margin-bottom: 12px;
          cursor: pointer;
        }

        .checkbox-label input[type="checkbox"] {
          margin-right: 8px;
          cursor: pointer;
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
          max-width: 200px;
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

        .actions {
          margin-top: 24px;
        }

        .btn-primary {
          padding: 12px 24px;
          background-color: #4CAF50;
          color: white;
          border: none;
          border-radius: 4px;
          font-size: 16px;
          font-weight: 500;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        .btn-primary:hover:not(:disabled) {
          background-color: #45a049;
        }

        .btn-primary:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .error-message {
          padding: 12px;
          margin-bottom: 16px;
          background-color: #ffebee;
          color: #c62828;
          border-radius: 4px;
        }

        .success-message {
          padding: 12px;
          margin-bottom: 16px;
          background-color: #e8f5e9;
          color: #2e7d32;
          border-radius: 4px;
        }
      `}</style>
    </div>
  );
};
