/**
 * NotificationList component
 * Displays a list of user notifications
 */

import React from 'react';
import type { Notification } from '../../types/notification';

export interface NotificationListProps {
  notifications: Notification[];
  onMarkAsRead: (notificationId: string) => void;
  onDelete: (notificationId: string) => void;
  loading?: boolean;
}

export const NotificationList: React.FC<NotificationListProps> = ({
  notifications,
  onMarkAsRead,
  onDelete,
  loading = false,
}) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minutes ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'reminder':
        return '🔔';
      case 'goal_deadline':
        return '⏰';
      case 'goal_completed':
        return '✅';
      case 'system':
        return 'ℹ️';
      default:
        return '📢';
    }
  };

  if (loading) {
    return (
      <div className="notification-list">
        <div className="loading">Loading notifications...</div>
      </div>
    );
  }

  if (notifications.length === 0) {
    return (
      <div className="notification-list">
        <div className="empty-state">
          <p>No notifications yet</p>
        </div>
      </div>
    );
  }

  return (
    <div className="notification-list">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`notification-item ${!notification.is_read ? 'unread' : ''}`}
        >
          <div className="notification-icon">
            {getNotificationIcon(notification.notification_type)}
          </div>
          
          <div className="notification-content">
            <div className="notification-header">
              <h4>{notification.title}</h4>
              <span className="notification-time">
                {formatDate(notification.scheduled_time)}
              </span>
            </div>
            
            {notification.message && (
              <p className="notification-message">{notification.message}</p>
            )}
          </div>

          <div className="notification-actions">
            {!notification.is_read && (
              <button
                onClick={() => onMarkAsRead(notification.id)}
                className="btn-mark-read"
                title="Mark as read"
              >
                ✓
              </button>
            )}
            <button
              onClick={() => onDelete(notification.id)}
              className="btn-delete"
              title="Delete"
            >
              ×
            </button>
          </div>
        </div>
      ))}

      <style>{`
        .notification-list {
          max-width: 600px;
          margin: 0 auto;
        }

        .loading, .empty-state {
          text-align: center;
          padding: 40px 20px;
          color: #666;
        }

        .notification-item {
          display: flex;
          gap: 12px;
          padding: 16px;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          margin-bottom: 12px;
          background-color: #fff;
          transition: all 0.2s;
        }

        .notification-item:hover {
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .notification-item.unread {
          background-color: #f0f8ff;
          border-left: 4px solid #4CAF50;
        }

        .notification-icon {
          font-size: 24px;
          flex-shrink: 0;
        }

        .notification-content {
          flex: 1;
          min-width: 0;
        }

        .notification-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          gap: 12px;
          margin-bottom: 4px;
        }

        .notification-header h4 {
          margin: 0;
          font-size: 16px;
          font-weight: 600;
          color: #333;
        }

        .notification-time {
          font-size: 12px;
          color: #999;
          white-space: nowrap;
        }

        .notification-message {
          margin: 4px 0 0;
          font-size: 14px;
          color: #666;
          line-height: 1.5;
        }

        .notification-actions {
          display: flex;
          gap: 8px;
          flex-shrink: 0;
        }

        .btn-mark-read, .btn-delete {
          width: 32px;
          height: 32px;
          border: none;
          border-radius: 4px;
          background-color: #f5f5f5;
          cursor: pointer;
          font-size: 18px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background-color 0.2s;
        }

        .btn-mark-read:hover {
          background-color: #4CAF50;
          color: white;
        }

        .btn-delete:hover {
          background-color: #f44336;
          color: white;
        }
      `}</style>
    </div>
  );
};
