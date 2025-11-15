# UI Forms Feature Documentation

## Overview

This document describes the UI forms implementation for goal/task entry and daily review functionality in Let's Manifest. The forms provide a complete CRUD (Create, Read, Update, Delete) interface for users to manage their goals and daily reviews.

## Features Implemented

### 1. Goals Management

#### Goal Form
- **Create New Goal**: Form to enter goal details including:
  - Title (required)
  - Description (optional)
  - Goal Type: Daily, Weekly, Monthly, or Yearly (required)
  - Category (optional, e.g., Health, Career, Personal)
  - Target Value and Unit (optional, for measurable goals)
  - Start Date and End Date (required)
  - Priority Level: 0-5 (None to High)
  - Status: Active, Completed, Paused, or Cancelled (edit only)

- **Edit Goal**: Update existing goals with all fields editable except dates
- **Validation**: Client-side validation for required fields and data types
- **Error Handling**: Clear error messages for validation failures and API errors

#### Goal List
- **Display Goals**: Shows all user goals with:
  - Title and description
  - Status, type, and priority badges
  - Category
  - Progress bar (if target value is set)
  - Start and end dates
  
- **Actions**:
  - Edit: Opens goal in edit mode
  - Delete: Confirms and deletes goal (with confirmation dialog)

### 2. Daily Reviews Management

#### Daily Review Form
- **Create New Review**: Form with multiple sections:
  
  **Basic Information:**
  - Review Date (required, defaults to today)
  
  **Daily Metrics:**
  - Mood Rating (1-10 scale)
  - Energy Level (1-10 scale)
  - Productivity Rating (1-10 scale)
  - Sleep Hours (0-24)
  - Sleep Quality (1-10 scale)
  - Water Intake (ml)
  
  **Reflections:**
  - Accomplishments
  - Challenges
  - Lessons Learned
  - Gratitude
  - Tomorrow's Intentions
  - Highlights

- **Edit Review**: Update existing reviews (date cannot be changed)
- **Validation**: Client-side validation for numeric ranges and required fields
- **Error Handling**: Clear error messages for validation failures and API errors

#### Daily Review List
- **Display Reviews**: Shows all user reviews with:
  - Date
  - Visual rating bars for metrics (mood, energy, productivity, sleep quality)
  - Sleep hours and water intake
  - All reflection sections with emojis
  
- **Actions**:
  - Edit: Opens review in edit mode
  - Delete: Confirms and deletes review (with confirmation dialog)

## Reusable Components

### Form Components

1. **Input Component** (`src/components/common/Input`)
   - Text, number, date inputs
   - Label, error message, helper text support
   - Accessibility: ARIA labels, error descriptions
   - Responsive design

2. **Select Component** (`src/components/common/Select`)
   - Dropdown selection
   - Label, error message, helper text support
   - Custom styled dropdown with arrow indicator
   - Accessibility: ARIA labels, keyboard navigation

3. **TextArea Component** (`src/components/common/TextArea`)
   - Multi-line text input
   - Resizable vertically
   - Label, error message, helper text support
   - Accessibility: ARIA labels

4. **Button Component** (`src/components/common/Button`)
   - Multiple variants: primary, secondary, danger, success
   - Loading state with spinner
   - Full width option
   - Accessibility: Focus states, disabled handling

## API Integration

### Services

1. **Goal Service** (`src/services/goalService.ts`)
   - `createGoal(data)`: Create new goal
   - `getGoals(params)`: List goals with filters and pagination
   - `getGoal(goalId)`: Get single goal
   - `updateGoal(goalId, data)`: Update goal
   - `deleteGoal(goalId)`: Delete goal
   - `addProgress(goalId, data)`: Add progress entry
   - `getGoalProgress(goalId, params)`: Get progress entries

2. **Daily Review Service** (`src/services/dailyReviewService.ts`)
   - `createReview(data)`: Create new review
   - `getReviews(params)`: List reviews with filters and pagination
   - `getReview(reviewId)`: Get single review
   - `updateReview(reviewId, data)`: Update review
   - `deleteReview(reviewId)`: Delete review

### API Client

- **Base Configuration** (`src/api/client.ts`)
  - Axios instance with base URL from environment
  - Request interceptor for authentication token
  - Response interceptor for error handling
  - Automatic 401 handling (token cleanup)

## Validation

### Client-Side Validation

**Goals:**
- Title: Required, max 255 characters
- Goal Type: Required, must be one of: daily, weekly, monthly, yearly
- Start Date: Required
- End Date: Required, must be after start date
- Target Value: Must be a valid number (if provided)
- Priority: 0-5 range

**Daily Reviews:**
- Review Date: Required
- Rating fields (mood, energy, productivity, sleep quality): 1-10 range
- Sleep Hours: 0-24 range
- Water Intake: Must be positive number

### Error Display
- Field-level errors shown below inputs
- Form-level errors shown at top of form
- Clear, actionable error messages
- Errors clear when field is corrected

## Accessibility Features

1. **Semantic HTML**
   - Proper form elements and labels
   - Heading hierarchy
   - Button types specified

2. **ARIA Attributes**
   - `aria-label` for icon buttons
   - `aria-invalid` for error states
   - `aria-describedby` for error messages and helper text
   - `role="alert"` for error messages
   - `role="progressbar"` for progress indicators

3. **Keyboard Navigation**
   - All interactive elements keyboard accessible
   - Focus indicators on all focusable elements
   - Tab order follows logical flow

4. **Screen Reader Support**
   - Labels associated with inputs
   - Required field indicators
   - Error announcements
   - Loading state announcements

## Responsive Design

### Breakpoints

- **Desktop** (> 768px):
  - Multi-column layouts for form fields
  - Side-by-side action buttons
  - Full-width cards in grid

- **Mobile** (≤ 768px):
  - Single-column form layouts
  - Stacked action buttons (full width)
  - Adjusted font sizes for readability
  - Touch-friendly button sizes

### Design Considerations

- Mobile-first approach
- Touch targets minimum 44x44px
- Readable font sizes on all devices
- Adequate spacing for touch interaction
- Horizontal scrolling avoided

## User Flow

### Creating a Goal

1. User clicks "+ New Goal" button
2. Form appears with empty fields
3. User fills required fields (title, goal type, dates)
4. User optionally fills additional fields
5. User clicks "Create Goal"
6. Validation runs; errors shown if any
7. If valid, API request sent
8. On success, form closes and goal appears in list
9. On error, error message shown; user can retry

### Editing a Goal

1. User clicks "Edit" button on a goal card
2. Form appears pre-filled with goal data
3. User modifies fields as needed
4. User clicks "Update Goal"
5. Validation runs; errors shown if any
6. If valid, API request sent
7. On success, form closes and goal updates in list
8. On error, error message shown; user can retry

### Similar flows for Daily Reviews

## State Management

### Component State
- Form data managed in component state
- Loading states for async operations
- Error states for form and API errors
- Show/hide form state
- Editing item state

### Data Flow
1. User interaction triggers state change
2. State change triggers re-render
3. Form submission triggers API call
4. API response updates list data
5. UI re-renders with updated data

## Error Handling

### Types of Errors Handled

1. **Validation Errors**
   - Field-level validation
   - Form-level validation
   - Real-time feedback

2. **API Errors**
   - Network errors
   - Server errors (500)
   - Authentication errors (401)
   - Not found errors (404)
   - Validation errors from backend (422)

3. **User Feedback**
   - Error banners for critical errors
   - Field-level error messages
   - Loading indicators during operations
   - Success feedback (implicit - form closes, data refreshes)

## Testing Considerations

### Manual Testing Checklist

**Goals:**
- [ ] Create goal with all fields
- [ ] Create goal with minimal fields
- [ ] Edit goal
- [ ] Delete goal (with confirmation)
- [ ] Validation: empty title
- [ ] Validation: end date before start date
- [ ] Validation: invalid target value
- [ ] Cancel form (data not saved)
- [ ] API error handling

**Daily Reviews:**
- [ ] Create review with all fields
- [ ] Create review with minimal fields
- [ ] Edit review
- [ ] Delete review (with confirmation)
- [ ] Validation: empty date
- [ ] Validation: ratings out of range
- [ ] Validation: negative water intake
- [ ] Cancel form (data not saved)
- [ ] API error handling

**Responsive Design:**
- [ ] Test on desktop (> 768px)
- [ ] Test on tablet (768px)
- [ ] Test on mobile (< 768px)
- [ ] Test form layout responsiveness
- [ ] Test list layout responsiveness

**Accessibility:**
- [ ] Keyboard navigation through form
- [ ] Focus indicators visible
- [ ] Screen reader announcements
- [ ] Error messages read by screen reader
- [ ] Required field indicators

## Future Enhancements

1. **Form Improvements**
   - Auto-save drafts
   - Rich text editor for descriptions
   - Date picker with calendar UI
   - Recurring goals support
   - Bulk operations (delete multiple, bulk edit)

2. **Validation**
   - Server-side validation feedback integration
   - Custom validation rules per goal type
   - Cross-field validation

3. **UX Enhancements**
   - Toast notifications for success
   - Undo delete functionality
   - Inline editing for quick updates
   - Drag-and-drop reordering
   - Search and filter UI

4. **Advanced Features**
   - Goal templates
   - Progress charts and visualizations
   - Goal reminders/notifications
   - Goal sharing/collaboration
   - Export/import functionality

## Technical Notes

### Dependencies
- React 19.2.0
- TypeScript 5.9.3
- Axios 1.13.2
- React Router DOM 7.9.6

### File Structure
```
frontend/src/
├── api/
│   └── client.ts                 # Axios configuration
├── components/
│   ├── common/                   # Reusable form components
│   │   ├── Input/
│   │   ├── Select/
│   │   ├── TextArea/
│   │   └── Button/
│   ├── Goals/                    # Goal-specific components
│   │   ├── GoalForm.tsx
│   │   └── GoalList.tsx
│   └── Review/                   # Review-specific components
│       ├── DailyReviewForm.tsx
│       └── DailyReviewList.tsx
├── pages/
│   ├── Goals/                    # Goals page
│   └── Review/                   # Review page
├── services/
│   ├── goalService.ts            # Goal API calls
│   └── dailyReviewService.ts    # Review API calls
└── types/
    ├── api.ts                    # Common API types
    ├── goal.ts                   # Goal types
    └── dailyReview.ts           # Review types
```

## Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=Let's Manifest
```

### API Base URL
- Development: `http://localhost:8000/api/v1`
- Production: Update to production API URL

## Getting Started

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Access the application:**
   - Open browser to `http://localhost:5173`
   - Navigate to `/goals` for Goals page
   - Navigate to `/review` for Daily Review page

5. **Build for production:**
   ```bash
   npm run build
   ```

## Support

For issues or questions:
- Check the main README.md
- Review API documentation in `/docs/api/`
- Check backend README for API setup
- Create an issue on GitHub

## License

MIT License - See LICENSE file for details
