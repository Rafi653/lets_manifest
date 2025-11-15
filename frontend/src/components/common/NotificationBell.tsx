/**
 * NotificationBell component
 * Displays notification bell icon with unread count badge
 */

import React, { useState } from 'react';
import { useNotifications } from '../../hooks/useNotifications';
import { NotificationList } from './NotificationList';

export const NotificationBell: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const {
    notifications,
    unreadCount,
    loading,
    markAsRead,
    deleteNotification,
    fetchNotifications,
    fetchUnreadCount,
  } = useNotifications({
    autoFetch: true,
    limit: 10,
  });

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      fetchNotifications();
      fetchUnreadCount();
    }
  };

  const handleMarkAsRead = async (notificationId: string) => {
    await markAsRead(notificationId);
  };

  const handleDelete = async (notificationId: string) => {
    await deleteNotification(notificationId);
  };

  return (
    <div className="notification-bell-container">
      <button
        className="notification-bell-button"
        onClick={toggleDropdown}
        aria-label="Notifications"
      >
        <span className="bell-icon">🔔</span>
        {unreadCount > 0 && (
          <span className="badge">{unreadCount > 9 ? '9+' : unreadCount}</span>
        )}
      </button>

      {isOpen && (
        <>
          <div className="notification-overlay" onClick={toggleDropdown} />
          <div className="notification-dropdown">
            <div className="dropdown-header">
              <h3>Notifications</h3>
              <button className="close-button" onClick={toggleDropdown}>
                ×
              </button>
            </div>

            <div className="dropdown-content">
              <NotificationList
                notifications={notifications}
                onMarkAsRead={handleMarkAsRead}
                onDelete={handleDelete}
                loading={loading}
              />
            </div>

            {notifications.length > 0 && (
              <div className="dropdown-footer">
                <a href="/notifications">View All Notifications</a>
              </div>
            )}
          </div>
        </>
      )}

      <style>{`
        .notification-bell-container {
          position: relative;
        }

        .notification-bell-button {
          position: relative;
          background: none;
          border: none;
          cursor: pointer;
          padding: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .bell-icon {
          font-size: 24px;
        }

        .badge {
          position: absolute;
          top: 4px;
          right: 4px;
          background-color: #f44336;
          color: white;
          border-radius: 10px;
          padding: 2px 6px;
          font-size: 10px;
          font-weight: bold;
          min-width: 18px;
          text-align: center;
        }

        .notification-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          z-index: 999;
        }

        .notification-dropdown {
          position: absolute;
          top: 100%;
          right: 0;
          width: 400px;
          max-height: 600px;
          background-color: white;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
          z-index: 1000;
          margin-top: 8px;
          display: flex;
          flex-direction: column;
        }

        @media (max-width: 480px) {
          .notification-dropdown {
            width: 100vw;
            right: -8px;
            max-height: 80vh;
          }
        }

        .dropdown-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 16px;
          border-bottom: 1px solid #e0e0e0;
        }

        .dropdown-header h3 {
          margin: 0;
          font-size: 18px;
          font-weight: 600;
        }

        .close-button {
          background: none;
          border: none;
          font-size: 28px;
          cursor: pointer;
          color: #666;
          line-height: 1;
          padding: 0;
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .close-button:hover {
          color: #333;
        }

        .dropdown-content {
          flex: 1;
          overflow-y: auto;
          padding: 8px;
        }

        .dropdown-footer {
          padding: 12px 16px;
          border-top: 1px solid #e0e0e0;
          text-align: center;
        }

        .dropdown-footer a {
          color: #4CAF50;
          text-decoration: none;
          font-weight: 500;
        }

        .dropdown-footer a:hover {
          text-decoration: underline;
        }
      `}</style>
    </div>
  );
};
