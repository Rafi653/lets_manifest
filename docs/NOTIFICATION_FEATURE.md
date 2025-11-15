# Notification & Scheduling Feature - Implementation Guide

## Overview

This document provides guidance on integrating the notification and scheduling feature into the Let's Manifest application.

## Feature Description

The notification system allows users to:
- Set reminders for goals with customizable time and frequency
- Receive browser notifications (with permission)
- Manage notification preferences (email, browser)
- View and manage notification history
- Configure default reminder settings

## Architecture

### Backend Components

**Models:**
- `Notification`: Stores individual notifications with scheduling info
- `NotificationSettings`: User-specific notification preferences
- Enhanced `Goal` model with reminder fields

**Services:**
- `NotificationService`: Business logic for notifications
- Auto-creates reminders when goals are saved with reminders enabled
- Provides batch processing for pending notifications

**API Endpoints:**
```
POST   /api/v1/notifications                    - Create notification
GET    /api/v1/notifications                    - List notifications
GET    /api/v1/notifications/{id}               - Get notification
PUT    /api/v1/notifications/{id}               - Update notification
POST   /api/v1/notifications/{id}/read          - Mark as read
DELETE /api/v1/notifications/{id}               - Delete notification
GET    /api/v1/notifications/settings/me        - Get settings
POST   /api/v1/notifications/settings           - Create settings
PUT    /api/v1/notifications/settings/me        - Update settings
```

### Frontend Components

**Services:**
- `notificationService`: API client with browser notification support

**Hooks:**
- `useNotifications`: State management for notifications

**UI Components:**
- `ReminderSettings`: Goal form component for reminder configuration
- `NotificationList`: Displays list of notifications
- `NotificationPreferences`: User settings page
- `NotificationBell`: Header component with unread badge

## Setup Instructions

### 1. Database Migration

Run the Alembic migration to create the new tables:

```bash
cd backend
alembic upgrade head
```

This will:
- Create `notifications` table
- Create `notification_settings` table
- Add reminder fields to `goals` table

### 2. Integrate UI Components

#### Add Reminder Settings to Goal Forms

In your goal creation/edit form component:

```tsx
import { ReminderSettings } from './components/Goals/ReminderSettings';

// In your form state
const [formData, setFormData] = useState({
  // ... other fields
  reminder_enabled: false,
  reminder_time: '09:00',
  reminder_days_before: 1,
});

// In your form JSX
<ReminderSettings
  reminderEnabled={formData.reminder_enabled}
  reminderTime={formData.reminder_time}
  reminderDaysBefore={formData.reminder_days_before}
  onReminderEnabledChange={(enabled) => 
    setFormData({...formData, reminder_enabled: enabled})}
  onReminderTimeChange={(time) => 
    setFormData({...formData, reminder_time: time})}
  onReminderDaysBeforeChange={(days) => 
    setFormData({...formData, reminder_days_before: days})}
/>
```

#### Add Notification Bell to Header

In your app header/navbar component:

```tsx
import { NotificationBell } from './components/common/NotificationBell';

// In your header JSX
<header>
  {/* ... other header elements */}
  <NotificationBell />
</header>
```

#### Add Notification Settings Page

In your router configuration:

```tsx
import { NotificationPreferences } from './components/common/NotificationPreferences';

// Add route
<Route path="/settings/notifications" element={<NotificationPreferences />} />
```

### 3. Set Up Notification Processing (Optional)

For production, implement a background worker to process pending notifications:

```python
from app.services.notification_service import NotificationService
from app.core.database import get_db

async def process_notifications():
    """Background task to process pending notifications."""
    async for db in get_db():
        service = NotificationService(db)
        count = await service.process_pending_notifications()
        print(f"Processed {count} notifications")
```

Schedule this using:
- **APScheduler** (simple, good for single-server setups)
- **Celery** (distributed task queue, good for scale)
- **Cron job** (basic scheduling)

Example with APScheduler:

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(process_notifications, 'interval', minutes=5)
scheduler.start()
```

## Usage Examples

### Creating a Goal with Reminder

```python
# Backend
goal_data = GoalCreate(
    title="Complete Project",
    goal_type="weekly",
    start_date="2025-11-20",
    end_date="2025-11-27",
    reminder_enabled=True,
    reminder_time="09:00",
    reminder_days_before=1
)
```

```tsx
// Frontend
const goal = await goalService.createGoal({
  title: "Complete Project",
  goal_type: "weekly",
  start_date: "2025-11-20",
  end_date: "2025-11-27",
  reminder_enabled: true,
  reminder_time: "09:00",
  reminder_days_before: 1
});
```

### Fetching Notifications

```tsx
import { useNotifications } from './hooks/useNotifications';

function MyComponent() {
  const {
    notifications,
    unreadCount,
    loading,
    markAsRead,
    deleteNotification
  } = useNotifications({ autoFetch: true });

  return (
    <div>
      <p>Unread: {unreadCount}</p>
      {notifications.map(n => (
        <div key={n.id}>
          <p>{n.title}</p>
          <button onClick={() => markAsRead(n.id)}>Mark Read</button>
        </div>
      ))}
    </div>
  );
}
```

### Browser Notifications

```tsx
import { notificationService } from './services/notificationService';

// Request permission
const hasPermission = await notificationService.requestPermission();

// Show notification
if (hasPermission) {
  notificationService.showBrowserNotification('Goal Reminder', {
    body: 'Your goal deadline is tomorrow!',
    icon: '/icon.png'
  });
}
```

## Configuration Options

### Notification Types

- `reminder`: Goal reminders
- `goal_deadline`: Deadline warnings  
- `goal_completed`: Completion notifications
- `system`: System messages

### Notification Statuses

- `pending`: Not yet sent
- `sent`: Successfully sent
- `failed`: Failed to send
- `cancelled`: Cancelled by user

### User Settings

Users can configure:
- Email notifications (enabled/disabled)
- Email reminders (enabled/disabled)
- Email goal updates (enabled/disabled)
- Browser notifications (enabled/disabled)
- Browser reminders (enabled/disabled)
- Default reminder time (HH:MM)
- Default reminder hours before deadline

## Testing

### Backend Tests

Run the test suite:

```bash
cd backend
pytest tests/integration/test_notification_crud.py -v
pytest tests/unit/test_notification_service.py -v
```

Test coverage:
- Notification CRUD operations
- Notification settings management
- Goal reminder creation
- Cascade deletions
- Constraint validations

### Frontend Testing

Manual testing checklist:
- [ ] Create goal with reminder enabled
- [ ] Verify reminder settings appear in form
- [ ] Check notification bell shows unread count
- [ ] Mark notification as read
- [ ] Delete notification
- [ ] Update notification settings
- [ ] Request browser notification permission
- [ ] Verify browser notification appears

## Security Considerations

✅ **No vulnerabilities found** in CodeQL analysis

Best practices implemented:
- SQL injection prevention via ORM
- Input validation with Pydantic schemas
- User authorization checks in all endpoints
- Proper error handling
- No sensitive data in notifications

## Performance Considerations

- Notifications are indexed by user_id, scheduled_time, and notification_type
- Pagination implemented for notification lists
- Lazy loading of notification relationships
- Efficient queries with proper indexes

## Troubleshooting

### Notifications not appearing

1. Check database migration ran successfully
2. Verify goal has `reminder_enabled=True`
3. Check `reminder_time` is set
4. Ensure scheduled time is in the future

### Browser notifications not working

1. Verify permission granted: `Notification.permission === 'granted'`
2. Check HTTPS (required by browsers)
3. Verify browser supports Notifications API
4. Check user settings: `browser_enabled` and `browser_reminders`

### Background processing not running

1. Verify scheduler is configured and started
2. Check database connection in background task
3. Review logs for errors
4. Ensure `process_pending_notifications()` is being called

## Future Enhancements

Potential improvements:
- WebSocket/SSE for real-time notifications
- Push notifications for mobile apps
- SMS notifications
- Recurring notification patterns
- Notification templates
- Bulk notification actions
- Advanced filtering and search
- Notification analytics

## Support

For issues or questions:
- Review test files for usage examples
- Check API documentation at `/docs`
- Review code comments in service files
- File issues on GitHub

## License

This feature is part of the Let's Manifest project and follows the same license.
