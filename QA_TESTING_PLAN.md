# QA/Testing Plan for Let's Manifest 🌟

## Table of Contents
1. [Overview](#overview)
2. [Testing Strategy](#testing-strategy)
3. [Test Coverage](#test-coverage)
4. [Test Frameworks and Tools](#test-frameworks-and-tools)
5. [Acceptance Scenarios](#acceptance-scenarios)
6. [Edge Cases and Error Handling](#edge-cases-and-error-handling)
7. [Integration and E2E Testing](#integration-and-e2e-testing)
8. [QA Workflow](#qa-workflow)
9. [Test Tracking](#test-tracking)
10. [CI/CD Integration](#cicd-integration)
11. [Reporting and Metrics](#reporting-and-metrics)

---

## Overview

### Purpose
This document outlines the comprehensive QA and testing strategy for the Let's Manifest application, a full-stack manifestation journaling platform built with React (frontend) and FastAPI/Python (backend).

### Quality Goals
- **Reliability**: Ensure the application works consistently across all supported environments
- **Performance**: Maintain fast response times and smooth user experience
- **Security**: Protect user data and prevent vulnerabilities
- **Usability**: Verify intuitive user interface and workflows
- **Maintainability**: Write tests that are easy to understand and maintain

### Scope
- **Frontend**: React components, user interactions, routing, state management
- **Backend**: API endpoints, business logic, data validation, authentication
- **Integration**: Full user workflows from frontend to backend to database
- **E2E**: Critical user journeys across the entire application

---

## Testing Strategy

### Testing Pyramid
We follow the standard testing pyramid approach:

```
        /\
       /  \
      / E2E \         10-15% of tests
     /______\
    /        \
   / Integration \    20-30% of tests
  /______________\
 /                \
/   Unit Tests     \   55-70% of tests
/____________________\
```

### Test Levels

#### 1. Unit Tests (55-70%)
- **Purpose**: Test individual functions, methods, and components in isolation
- **Speed**: Fast (milliseconds)
- **Scope**: Single function/component
- **Examples**:
  - React component rendering
  - API service functions
  - Utility functions
  - Data validation logic
  - Business logic calculations

#### 2. Integration Tests (20-30%)
- **Purpose**: Test interaction between multiple components/modules
- **Speed**: Medium (seconds)
- **Scope**: Multiple components working together
- **Examples**:
  - API endpoint with database operations
  - Frontend components with API services
  - Authentication flow
  - Data persistence workflows

#### 3. End-to-End Tests (10-15%)
- **Purpose**: Test complete user workflows
- **Speed**: Slow (seconds to minutes)
- **Scope**: Entire application stack
- **Examples**:
  - User registration and login
  - Creating and viewing manifestations
  - Complete goal tracking workflow
  - Dashboard visualization

### Test Types

#### Functional Testing
- Feature functionality validation
- User workflow testing
- Form validation
- Navigation and routing
- Data CRUD operations

#### Non-Functional Testing
- **Performance**: Response times, load testing
- **Security**: Authentication, authorization, input validation, SQL injection prevention
- **Usability**: UI/UX consistency, accessibility (WCAG 2.1)
- **Compatibility**: Browser compatibility (Chrome, Firefox, Safari, Edge)
- **Responsiveness**: Mobile, tablet, desktop layouts

#### Regression Testing
- Automated test suite run on every commit
- Manual smoke testing for releases
- Verification of bug fixes

---

## Test Coverage

### Target Coverage Metrics

#### Backend (Python/FastAPI)
- **Overall Code Coverage**: 80% minimum
- **Critical Paths**: 95% minimum
  - Authentication and authorization
  - Data persistence
  - Business logic calculations
- **API Endpoints**: 100% coverage
- **Models and Schemas**: 90% coverage

#### Frontend (React/TypeScript)
- **Overall Code Coverage**: 75% minimum
- **Critical Components**: 90% minimum
  - Authentication forms
  - Data entry forms
  - Core dashboard components
- **Utility Functions**: 85% coverage
- **API Services**: 90% coverage

### Coverage Areas

#### Backend Coverage

##### 1. API Endpoints (All modules)
- **Authentication** (`/api/v1/auth`)
  - ✅ User registration
  - ✅ User login
  - ✅ Token refresh
  - ✅ Logout
  - ✅ Password reset

- **Users** (`/api/v1/users`)
  - ✅ Get current user profile
  - ✅ Update user profile
  - ✅ Delete user account
  - ✅ User preferences

- **Goals** (`/api/v1/goals`)
  - ✅ List goals (with pagination, filtering)
  - ✅ Create goal
  - ✅ Get goal by ID
  - ✅ Update goal
  - ✅ Delete goal
  - ✅ Add progress entry
  - ✅ Get progress history

- **Habits** (`/api/v1/habits`)
  - ✅ List habits
  - ✅ Create habit
  - ✅ Get habit by ID
  - ✅ Update habit
  - ✅ Delete habit
  - ✅ Create habit entry (check-in)
  - ✅ Get habit entries with statistics

- **Food Tracking** (`/api/v1/foods`)
  - ✅ List food entries (with date filtering)
  - ✅ Create food entry
  - ✅ Get food entry by ID
  - ✅ Update food entry
  - ✅ Delete food entry
  - ✅ Nutrition summary calculations

- **Workouts** (`/api/v1/workouts`)
  - ✅ List workouts (with date filtering)
  - ✅ Create workout with exercises
  - ✅ Get workout by ID
  - ✅ Update workout
  - ✅ Delete workout
  - ✅ Workout statistics

- **Daily Reviews** (`/api/v1/daily-reviews`)
  - ✅ List daily reviews
  - ✅ Create daily review
  - ✅ Get daily review by ID
  - ✅ Update daily review
  - ✅ Delete daily review
  - ✅ Review analytics

- **Blog Entries** (`/api/v1/blog-entries`)
  - ✅ List blog entries (public/private filtering)
  - ✅ Create blog entry
  - ✅ Get blog entry by ID
  - ✅ Update blog entry
  - ✅ Delete blog entry
  - ✅ Publish/unpublish

- **Progress Tracking** (`/api/v1/progress`)
  - ✅ List progress snapshots
  - ✅ Create progress snapshot
  - ✅ Get snapshot by ID
  - ✅ Update snapshot
  - ✅ Delete snapshot
  - ✅ Trend analysis

- **Notifications** (`/api/v1/notifications`)
  - ✅ List notifications
  - ✅ Mark as read
  - ✅ Delete notifications
  - ✅ Notification preferences

- **Analytics**
  - ✅ Habit analytics and streaks
  - ✅ Goal analytics and completion rates
  - ✅ Life goals analytics
  - ✅ Overall progress metrics

##### 2. Models and Database
- Schema validation
- Database constraints
- Relationship integrity
- Migration testing

##### 3. Business Logic
- Data calculations
- Validation rules
- Business rule enforcement
- Authorization logic

##### 4. Security
- JWT token generation and validation
- Password hashing and verification
- Input sanitization
- SQL injection prevention
- CORS configuration

#### Frontend Coverage

##### 1. Components
- **Authentication Components**
  - Login form
  - Registration form
  - Password reset form
  - Protected route component

- **Layout Components**
  - Navigation bar
  - Sidebar
  - Footer
  - Page layout wrapper

- **Dashboard Components**
  - Goal cards
  - Habit tracker
  - Progress charts
  - Activity feed
  - Quick stats

- **Form Components**
  - Goal creation/edit form
  - Habit creation/edit form
  - Food entry form
  - Workout entry form
  - Daily review form
  - Blog entry editor

- **List/Table Components**
  - Goals list with filters
  - Habits list
  - Food log table
  - Workout history
  - Blog entries list

- **Common/Shared Components**
  - Modal dialogs
  - Buttons
  - Input fields
  - Date pickers
  - Toast notifications
  - Loading spinners
  - Error boundaries

##### 2. Services/API Layer
- API client configuration
- Authentication service
- Goal service
- Habit service
- Food service
- Workout service
- Blog service
- Error handling and retries

##### 3. State Management
- Context providers
- Custom hooks
- State updates
- Side effects

##### 4. Routing
- Route configuration
- Protected routes
- Navigation flows
- 404 handling

##### 5. Utilities
- Date formatting
- Data validation
- Helper functions
- Constants

---

## Test Frameworks and Tools

### Backend Testing Stack

#### Core Frameworks
```python
# requirements-dev.txt
pytest==7.4.3              # Test framework
pytest-asyncio==0.21.1     # Async test support
pytest-cov==4.1.0          # Coverage reporting
httpx==0.25.1              # HTTP client for API testing
faker==20.1.0              # Test data generation
```

#### Testing Tools
- **pytest**: Primary test framework
- **pytest-asyncio**: For testing async FastAPI endpoints
- **pytest-cov**: Code coverage measurement
- **httpx**: Testing HTTP requests/responses
- **Faker**: Generating realistic test data
- **unittest.mock**: Mocking dependencies

#### Running Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test types
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests only

# Run specific test file
pytest tests/unit/test_auth.py

# Run with verbose output
pytest -v

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

### Frontend Testing Stack (Recommended)

#### Core Frameworks
```json
// package.json devDependencies
{
  "vitest": "^1.0.0",                    // Fast test runner (Vite-based)
  "@testing-library/react": "^14.0.0",   // React component testing
  "@testing-library/jest-dom": "^6.0.0", // Custom Jest matchers
  "@testing-library/user-event": "^14.0.0", // User interaction simulation
  "jsdom": "^23.0.0",                    // DOM implementation for Node
  "@vitest/ui": "^1.0.0",                // UI for test results
  "c8": "^8.0.0"                         // Coverage reporting
}
```

#### Testing Tools
- **Vitest**: Modern, fast test runner (recommended for Vite projects)
- **React Testing Library**: Component testing with user-centric approach
- **Testing Library User Event**: Realistic user interactions
- **MSW (Mock Service Worker)**: API mocking
- **Playwright/Cypress**: E2E testing (choose one)

#### Running Frontend Tests (when implemented)
```bash
# Run all tests
npm run test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch

# Run E2E tests
npm run test:e2e
```

### E2E Testing Tools

#### Recommended: Playwright
```json
// package.json
{
  "@playwright/test": "^1.40.0"
}
```

**Advantages**:
- Fast and reliable
- Cross-browser support (Chrome, Firefox, Safari, Edge)
- Built-in test runner
- Auto-wait for elements
- Network interception
- Parallel execution

**Alternative: Cypress**
- Developer-friendly API
- Time-travel debugging
- Real-time reloading
- Automatic screenshots and videos

### Additional Tools

#### Code Quality
- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **Black**: Python code formatting
- **Ruff**: Fast Python linter
- **mypy**: Python type checking

#### Performance Testing
- **Locust**: Load testing for backend APIs
- **Lighthouse**: Frontend performance auditing
- **WebPageTest**: Real-world performance metrics

#### Security Testing
- **Bandit**: Python security linter
- **OWASP ZAP**: Security vulnerability scanning
- **npm audit**: Frontend dependency security

#### Accessibility Testing
- **axe-core**: Automated accessibility testing
- **Pa11y**: Accessibility testing tool
- **WAVE**: Browser extension for accessibility

---

## Acceptance Scenarios

### Core User Journeys

#### 1. User Registration and Authentication
**Scenario**: New user creates an account
- User navigates to registration page
- User enters email, username, password, and profile details
- System validates input (email format, password strength, unique email/username)
- System creates account and sends welcome email
- User is redirected to login page
- User logs in with credentials
- System returns JWT token
- User is redirected to dashboard

**Acceptance Criteria**:
- ✅ Registration form validates all inputs
- ✅ Email must be unique and valid format
- ✅ Password must meet strength requirements (8+ chars, mixed case, numbers, symbols)
- ✅ Username must be unique and 3-20 characters
- ✅ JWT token is generated and stored securely
- ✅ User session persists on page refresh
- ✅ Appropriate error messages for validation failures

#### 2. Goal Creation and Tracking
**Scenario**: User creates and tracks a goal
- User clicks "New Goal" button
- User fills in goal details:
  - Title (required)
  - Description
  - Goal type (daily/weekly/monthly/yearly)
  - Category (fitness/career/health/personal/financial)
  - Target value and unit
  - Start and end dates
  - Priority level
- User submits the form
- System creates goal and displays it in goals list
- User adds progress entries over time
- System calculates completion percentage
- User views progress history and charts

**Acceptance Criteria**:
- ✅ Goal form validates required fields
- ✅ Goal appears in user's goals list
- ✅ Progress can be added with date, value, and notes
- ✅ Completion percentage is calculated correctly
- ✅ Goals can be filtered by type, category, status
- ✅ Goals can be edited and deleted
- ✅ Progress history is displayed with charts

#### 3. Habit Tracking
**Scenario**: User creates and maintains a habit
- User creates a new habit with name, description, frequency
- User checks in daily/weekly as per frequency
- System tracks streak and completion rate
- System sends reminders based on schedule
- User views habit statistics and trends

**Acceptance Criteria**:
- ✅ Habit is created with correct frequency
- ✅ Check-ins are recorded with timestamp
- ✅ Current streak is calculated correctly
- ✅ Best streak is tracked
- ✅ Completion rate is accurate
- ✅ Visual calendar shows check-in history
- ✅ Notifications work for habit reminders

#### 4. Food and Workout Logging
**Scenario**: User logs daily nutrition and exercise
- User logs food entries for meals with nutritional info
- System calculates daily nutrition totals
- User logs workout with exercises, sets, reps, weight
- System tracks workout statistics
- User views nutrition and workout history
- User sees trends and insights

**Acceptance Criteria**:
- ✅ Food entries include meal type, time, calories, macros
- ✅ Daily nutrition summary is calculated
- ✅ Workout includes multiple exercises with details
- ✅ Workout duration and intensity are tracked
- ✅ Historical data can be filtered and sorted
- ✅ Charts display trends over time

#### 5. Daily Review and Reflection
**Scenario**: User completes daily review
- User fills in daily review form:
  - Mood rating (1-10)
  - Energy level (1-10)
  - Productivity rating (1-10)
  - Sleep hours and quality
  - Accomplishments
  - Gratitude notes
  - Challenges faced
  - Tomorrow's priorities
- System saves review
- User views review history
- System generates weekly/monthly insights

**Acceptance Criteria**:
- ✅ All rating fields accept 1-10 values
- ✅ Text fields allow rich content
- ✅ One review per day allowed
- ✅ Historical reviews are accessible
- ✅ Average ratings are calculated
- ✅ Insights identify patterns and trends

#### 6. Blog/Journal Entries
**Scenario**: User creates manifestation journal entry
- User creates new blog entry
- User writes content with formatting
- User adds tags and categories
- User sets visibility (public/private)
- User publishes entry
- Entry appears in user's journal
- Public entries are visible to others (if applicable)

**Acceptance Criteria**:
- ✅ Rich text editor works correctly
- ✅ Draft saving functionality works
- ✅ Tags can be created and assigned
- ✅ Privacy settings are respected
- ✅ Entries can be edited and deleted
- ✅ Search and filtering work

#### 7. Analytics Dashboard
**Scenario**: User views progress analytics
- User navigates to analytics dashboard
- System displays:
  - Goal completion rates
  - Habit streaks and trends
  - Workout frequency and volume
  - Nutrition averages
  - Mood and energy trends
  - Overall progress score
- User filters by date range
- User exports data

**Acceptance Criteria**:
- ✅ All metrics are calculated correctly
- ✅ Charts render properly
- ✅ Data updates in real-time
- ✅ Filters work across all widgets
- ✅ Export includes all data in CSV/PDF format
- ✅ Performance is acceptable with large datasets

---

## Edge Cases and Error Handling

### Input Validation Edge Cases

#### 1. Authentication
- Empty email/password fields
- Invalid email format (missing @, invalid domain)
- Password too short (<8 chars)
- Password without required complexity
- Email already registered
- Username already taken
- Special characters in username
- SQL injection attempts in input fields
- XSS attempts in input fields

#### 2. Goal Creation
- Extremely long title (>200 chars)
- Missing required fields
- Invalid date ranges (end date before start date)
- Negative target values
- Target value with invalid unit
- Dates in the far past/future
- Special characters and emojis in text fields
- Very large numeric values (overflow)

#### 3. Data Entry
- Duplicate entries (same date/time)
- Future dates for historical data
- Negative values where inappropriate
- Zero values where invalid
- Extremely large values
- Invalid date formats
- Timezone handling
- Decimal precision handling

### Error Scenarios

#### 1. Network Errors
- **Offline mode**: Graceful degradation, queue actions
- **Timeout**: Retry with exponential backoff
- **500 Server Error**: Show user-friendly message, log error
- **Network interruption**: Handle mid-request failures
- **Slow connection**: Show loading states, don't block UI

#### 2. Authentication Errors
- **401 Unauthorized**: Redirect to login, clear token
- **403 Forbidden**: Show permission error
- **Token expired**: Refresh token automatically or redirect to login
- **Invalid credentials**: Clear, helpful error message
- **Rate limiting**: Show throttle message

#### 3. Data Errors
- **404 Not Found**: Resource doesn't exist or was deleted
- **409 Conflict**: Duplicate entry or version conflict
- **422 Validation Error**: Show field-specific errors
- **413 Payload Too Large**: File/data size limit
- **Database connection loss**: Retry, show error if persistent

#### 4. State Management Errors
- **Stale data**: Refresh data automatically
- **Optimistic update failure**: Rollback UI changes
- **Race conditions**: Prevent concurrent updates
- **Cache invalidation**: Clear cache on errors

### Boundary Testing

#### Numeric Boundaries
- Minimum values (0, 1)
- Maximum values (INT_MAX, system limits)
- Negative values
- Decimal precision (0.01, 0.001)
- Very large numbers (scientific notation)

#### String Boundaries
- Empty strings
- Single character
- Maximum length strings
- Unicode characters (emojis, special chars)
- Whitespace handling (leading, trailing, multiple spaces)
- HTML/Script tags
- SQL injection patterns

#### Date/Time Boundaries
- Leap years (February 29)
- Month end dates (28, 30, 31)
- Year boundaries (Dec 31 → Jan 1)
- Timezone changes (DST)
- Historical dates (very old)
- Future dates (far future)

#### Pagination Boundaries
- Page 1
- Last page
- Page beyond last
- Page 0 or negative
- Very large page numbers
- Limit of 0 or negative
- Limit larger than total items

### Performance Edge Cases
- Loading very large datasets (>10,000 items)
- Concurrent user actions
- Rapid successive API calls
- Large file uploads
- Complex database queries
- Memory-intensive operations

---

## Integration and E2E Testing

### Integration Test Coverage

#### Backend Integration Tests

##### 1. Database Integration
**Test**: API endpoint writes to database correctly
```python
async def test_create_goal_persists_to_database():
    # Create goal via API
    response = await client.post("/api/v1/goals", json=goal_data)
    goal_id = response.json()["data"]["id"]
    
    # Verify in database
    db_goal = await db.query(Goal).filter(Goal.id == goal_id).first()
    assert db_goal is not None
    assert db_goal.title == goal_data["title"]
```

##### 2. Authentication Flow
**Test**: Complete auth flow with JWT
```python
async def test_authentication_flow():
    # Register user
    register_response = await client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 201
    
    # Login
    login_response = await client.post("/api/v1/auth/login", json=credentials)
    token = login_response.json()["data"]["access_token"]
    
    # Access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = await client.get("/api/v1/users/me", headers=headers)
    assert profile_response.status_code == 200
```

##### 3. Data Relationships
**Test**: Related data is created and retrieved correctly
```python
async def test_goal_with_progress_entries():
    # Create goal
    goal = await create_test_goal()
    
    # Add progress entries
    await create_progress_entry(goal.id, value=25)
    await create_progress_entry(goal.id, value=50)
    
    # Retrieve goal with progress
    response = await client.get(f"/api/v1/goals/{goal.id}")
    goal_data = response.json()["data"]
    
    assert goal_data["completion_percentage"] == 50
    assert len(goal_data["progress_entries"]) == 2
```

##### 4. Business Logic
**Test**: Complex calculations work across modules
```python
async def test_habit_streak_calculation():
    habit = await create_test_habit()
    
    # Create check-ins for consecutive days
    for i in range(7):
        date = today - timedelta(days=i)
        await create_habit_entry(habit.id, date)
    
    # Get habit with statistics
    response = await client.get(f"/api/v1/habits/{habit.id}")
    stats = response.json()["data"]["statistics"]
    
    assert stats["current_streak"] == 7
    assert stats["completion_rate"] == 100
```

#### Frontend Integration Tests

##### 1. Component with API
**Test**: Component fetches and displays data
```typescript
test('Goals list fetches and displays goals', async () => {
  // Mock API response
  server.use(
    http.get('/api/v1/goals', () => {
      return HttpResponse.json({
        data: { items: mockGoals, total: 2 }
      })
    })
  )
  
  // Render component
  render(<GoalsList />)
  
  // Verify goals are displayed
  await waitFor(() => {
    expect(screen.getByText('Complete Marathon')).toBeInTheDocument()
    expect(screen.getByText('Learn Python')).toBeInTheDocument()
  })
})
```

##### 2. Form Submission
**Test**: Form validates and submits data
```typescript
test('Goal form validates and submits', async () => {
  const user = userEvent.setup()
  render(<GoalForm />)
  
  // Fill form
  await user.type(screen.getByLabelText('Title'), 'New Goal')
  await user.selectOptions(screen.getByLabelText('Type'), 'yearly')
  await user.type(screen.getByLabelText('Target'), '100')
  
  // Submit
  await user.click(screen.getByRole('button', { name: 'Create Goal' }))
  
  // Verify API call
  await waitFor(() => {
    expect(createGoalSpy).toHaveBeenCalledWith({
      title: 'New Goal',
      goal_type: 'yearly',
      target_value: 100
    })
  })
})
```

##### 3. Authentication Flow
**Test**: Login and route protection
```typescript
test('Protected route redirects unauthenticated users', () => {
  render(
    <MemoryRouter initialEntries={['/dashboard']}>
      <App />
    </MemoryRouter>
  )
  
  // Should redirect to login
  expect(screen.getByText('Login')).toBeInTheDocument()
})

test('Successful login redirects to dashboard', async () => {
  const user = userEvent.setup()
  render(<LoginForm />)
  
  // Fill and submit login form
  await user.type(screen.getByLabelText('Email'), 'user@example.com')
  await user.type(screen.getByLabelText('Password'), 'password123')
  await user.click(screen.getByRole('button', { name: 'Login' }))
  
  // Verify redirect
  await waitFor(() => {
    expect(window.location.pathname).toBe('/dashboard')
  })
})
```

### E2E Test Scenarios

#### Critical User Paths

##### 1. Complete Onboarding Flow
```typescript
// e2e/onboarding.spec.ts
test('User can register, login, and complete onboarding', async ({ page }) => {
  // Navigate to registration
  await page.goto('http://localhost:5173/register')
  
  // Fill registration form
  await page.fill('[name="email"]', 'newuser@example.com')
  await page.fill('[name="username"]', 'newuser')
  await page.fill('[name="password"]', 'SecurePass123!')
  await page.fill('[name="confirmPassword"]', 'SecurePass123!')
  await page.click('button:has-text("Register")')
  
  // Should redirect to login
  await page.waitForURL('**/login')
  
  // Login
  await page.fill('[name="email"]', 'newuser@example.com')
  await page.fill('[name="password"]', 'SecurePass123!')
  await page.click('button:has-text("Login")')
  
  // Should reach dashboard
  await page.waitForURL('**/dashboard')
  expect(await page.textContent('h1')).toContain('Dashboard')
})
```

##### 2. Goal Creation and Progress Tracking
```typescript
test('User can create goal and add progress', async ({ page }) => {
  await loginAsUser(page, testUser)
  
  // Navigate to goals
  await page.click('nav >> text=Goals')
  await page.click('button:has-text("New Goal")')
  
  // Create goal
  await page.fill('[name="title"]', 'Run 100 miles')
  await page.selectOption('[name="goalType"]', 'monthly')
  await page.fill('[name="targetValue"]', '100')
  await page.fill('[name="targetUnit"]', 'miles')
  await page.click('button:has-text("Create")')
  
  // Verify goal appears
  await expect(page.locator('text=Run 100 miles')).toBeVisible()
  
  // Add progress
  await page.click('text=Run 100 miles')
  await page.click('button:has-text("Add Progress")')
  await page.fill('[name="value"]', '25')
  await page.fill('[name="notes"]', 'Completed week 1')
  await page.click('button:has-text("Save Progress")')
  
  // Verify progress
  await expect(page.locator('text=25%')).toBeVisible()
})
```

##### 3. Habit Tracking Workflow
```typescript
test('User can create habit and check in', async ({ page }) => {
  await loginAsUser(page, testUser)
  
  // Create habit
  await page.click('nav >> text=Habits')
  await page.click('button:has-text("New Habit")')
  await page.fill('[name="name"]', 'Morning Meditation')
  await page.selectOption('[name="frequency"]', 'daily')
  await page.click('button:has-text("Create")')
  
  // Check in
  await page.click('[data-testid="habit-checkin-Morning Meditation"]')
  await expect(page.locator('text=Streak: 1 day')).toBeVisible()
  
  // Check in next day
  await mockDate(page, addDays(new Date(), 1))
  await page.reload()
  await page.click('[data-testid="habit-checkin-Morning Meditation"]')
  await expect(page.locator('text=Streak: 2 days')).toBeVisible()
})
```

##### 4. Multi-Module Integration
```typescript
test('Dashboard shows data from all modules', async ({ page }) => {
  await loginAsUser(page, testUser)
  await seedTestData(testUser)
  
  // Navigate to dashboard
  await page.goto('http://localhost:5173/dashboard')
  
  // Verify all sections
  await expect(page.locator('[data-testid="goals-summary"]')).toBeVisible()
  await expect(page.locator('[data-testid="habits-summary"]')).toBeVisible()
  await expect(page.locator('[data-testid="recent-workouts"]')).toBeVisible()
  await expect(page.locator('[data-testid="nutrition-summary"]')).toBeVisible()
  
  // Verify data accuracy
  const goalsCount = await page.textContent('[data-testid="active-goals-count"]')
  expect(goalsCount).toBe('5')
})
```

#### E2E Test Organization
```
e2e/
├── auth/
│   ├── registration.spec.ts
│   ├── login.spec.ts
│   └── password-reset.spec.ts
├── goals/
│   ├── create-goal.spec.ts
│   ├── update-goal.spec.ts
│   ├── track-progress.spec.ts
│   └── goal-filters.spec.ts
├── habits/
│   ├── create-habit.spec.ts
│   ├── habit-checkin.spec.ts
│   └── habit-streaks.spec.ts
├── health/
│   ├── food-logging.spec.ts
│   ├── workout-logging.spec.ts
│   └── daily-review.spec.ts
├── blog/
│   ├── create-entry.spec.ts
│   └── publish-entry.spec.ts
└── dashboard/
    ├── analytics.spec.ts
    └── overview.spec.ts
```

---

## QA Workflow

### Development Workflow

```
┌──────────────────┐
│  Feature Request │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Define AC       │  ← QA defines acceptance criteria
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Write Tests     │  ← QA/Dev write test cases
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Implementation  │  ← Dev implements feature
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Run Tests       │  ← Automated tests run
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Code Review     │  ← Review code + tests
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  QA Testing      │  ← Manual testing
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Deploy          │  ← Deploy to prod
└──────────────────┘
```

### Test Execution Flow

#### Pre-Commit
```bash
# Developer runs locally before commit
npm run lint           # Frontend linting
npm run type-check     # TypeScript checking
npm run test:unit      # Frontend unit tests

cd backend
black app/             # Python formatting
ruff check app/        # Python linting
pytest -m unit         # Backend unit tests
```

#### Continuous Integration (CI)
```yaml
# On every push/PR
1. Lint checks (frontend + backend)
2. Type checking
3. Unit tests (frontend + backend)
4. Integration tests (backend)
5. Component tests (frontend)
6. Security scans
7. Coverage reports
```

#### Pre-Release Testing
```bash
# Before release
1. Full test suite (unit + integration + E2E)
2. Manual exploratory testing
3. Performance testing
4. Accessibility testing
5. Cross-browser testing
6. Mobile responsiveness testing
7. Security scan
```

### Roles and Responsibilities

#### QA Engineer
- Define test strategy and test plans
- Write test cases and scenarios
- Execute manual tests
- Review automated tests
- Report bugs with detailed reproduction steps
- Verify bug fixes
- Sign off on releases
- Maintain test documentation

#### Developers
- Write unit and integration tests for their code
- Fix failing tests
- Maintain test coverage
- Review test code in PRs
- Assist with test infrastructure

#### Tech Lead
- Review test architecture
- Ensure test best practices
- Approve test coverage strategy
- Allocate resources for testing

#### Product Manager
- Define acceptance criteria
- Prioritize test scenarios
- Approve release based on QA sign-off

### Release QA Checklist

#### Pre-Release
- [ ] All automated tests passing
- [ ] No critical/high bugs
- [ ] Manual smoke testing completed
- [ ] Performance benchmarks met
- [ ] Security scan passed
- [ ] Accessibility audit passed
- [ ] Cross-browser testing completed
- [ ] Mobile testing completed
- [ ] Database migrations tested
- [ ] Rollback plan documented

#### Post-Release
- [ ] Monitoring alerts configured
- [ ] Smoke test in production
- [ ] User feedback monitoring
- [ ] Performance metrics review
- [ ] Error rate monitoring

---

## Test Tracking

### Test Case Template

```markdown
## Test Case: TC-001
**Module**: Goals
**Feature**: Create Goal
**Priority**: High
**Type**: Functional

### Description
Verify that a user can successfully create a new goal

### Pre-conditions
- User is logged in
- User has navigated to Goals page

### Test Steps
1. Click "New Goal" button
2. Enter "Complete Marathon" in title field
3. Select "Yearly" for goal type
4. Enter "42.195" for target value
5. Enter "km" for target unit
6. Click "Create" button

### Expected Results
- Goal is created successfully
- Success message is displayed
- Goal appears in goals list
- Goal has correct data
- Completion percentage shows 0%

### Actual Results
[To be filled during test execution]

### Status
[ ] Pass  [ ] Fail  [ ] Blocked  [ ] Not Executed

### Notes
[Any additional observations]
```

### Test Execution Tracking

#### Test Run Summary Template
```markdown
# Test Run: Release v1.0.0
**Date**: 2025-11-15
**Tester**: QA Team
**Environment**: Staging
**Build**: #123

## Summary
- Total Test Cases: 150
- Passed: 142
- Failed: 5
- Blocked: 3
- Not Executed: 0
- Pass Rate: 94.7%

## Failed Tests
| ID | Test Case | Module | Severity | Status |
|----|-----------|---------|----------|---------|
| TC-042 | Filter goals by date | Goals | Medium | Bug logged #456 |
| TC-089 | Export workout data | Workouts | Low | Bug logged #457 |
...

## Blocked Tests
| ID | Test Case | Reason | Action Required |
|----|-----------|--------|----------------|
| TC-101 | Payment integration | Feature not ready | Waiting for dev |
...

## Risk Assessment
- **High Risk**: None
- **Medium Risk**: Date filtering issue may affect user experience
- **Low Risk**: Export feature not critical for MVP

## Recommendation
✅ APPROVED for release with minor known issues documented
```

### Bug Report Template

```markdown
## Bug Report: BUG-001
**Reported By**: QA Tester
**Date**: 2025-11-15
**Severity**: High
**Priority**: P1
**Status**: Open
**Module**: Goals
**Environment**: Staging

### Summary
Goal completion percentage calculates incorrectly when progress exceeds target

### Steps to Reproduce
1. Login as test user
2. Create goal with target value 100
3. Add progress entry with value 150
4. View goal details

### Expected Behavior
Completion percentage should be capped at 100%

### Actual Behavior
Completion percentage shows 150%

### Screenshots
[Attach screenshots]

### Environment Details
- Browser: Chrome 120
- OS: Windows 11
- Backend Version: v1.0.0
- Frontend Version: v1.0.0

### Additional Information
- Happens with all goal types
- Database shows correct values
- Frontend calculation appears to be the issue

### Suggested Fix
Cap percentage calculation at 100% in the frontend component
```

### Test Metrics Dashboard

Track these metrics over time:

#### Test Execution Metrics
- **Total Tests**: Number of test cases
- **Pass Rate**: (Passed / Total) × 100
- **Test Execution Time**: Time to run full suite
- **Test Flakiness**: Number of intermittent failures

#### Code Coverage Metrics
- **Line Coverage**: Percentage of code lines executed
- **Branch Coverage**: Percentage of code branches executed
- **Function Coverage**: Percentage of functions called
- **Uncovered Critical Paths**: Critical code without tests

#### Defect Metrics
- **Defect Detection Rate**: Bugs found / Test cases executed
- **Defect Leakage**: Bugs found in production vs testing
- **Mean Time to Detection**: Average time to find a bug
- **Mean Time to Resolution**: Average time to fix a bug

#### Quality Metrics
- **Test Automation Rate**: Automated tests / Total tests
- **Test Maintenance Effort**: Time spent updating tests
- **Build Success Rate**: Percentage of successful CI builds
- **Release Frequency**: How often we can release confidently

---

## CI/CD Integration

### GitHub Actions Workflow

#### Recommended CI Pipeline
```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache Python dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt -r requirements-dev.txt
      
      - name: Lint with Ruff
        run: |
          cd backend
          ruff check app/
      
      - name: Format check with Black
        run: |
          cd backend
          black --check app/
      
      - name: Type check with mypy
        run: |
          cd backend
          mypy app/
        continue-on-error: true
      
      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
        run: |
          cd backend
          pytest --cov=app --cov-report=xml --cov-report=term -v
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Lint
        run: |
          cd frontend
          npm run lint
      
      - name: Type check
        run: |
          cd frontend
          npm run type-check
      
      - name: Run tests with coverage
        run: |
          cd frontend
          npm run test:coverage
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./frontend/coverage/coverage-final.json
          flags: frontend

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install Playwright
        run: |
          cd frontend
          npm ci
          npx playwright install --with-deps
      
      - name: Start services
        run: |
          docker-compose up -d
          sleep 10
      
      - name: Run E2E tests
        run: |
          cd frontend
          npm run test:e2e
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report

  security-scan:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Bandit security scan
        run: |
          cd backend
          pip install bandit
          bandit -r app/ -f json -o bandit-report.json || true
      
      - name: Run npm audit
        run: |
          cd frontend
          npm audit --json > npm-audit.json || true
      
      - name: Upload security reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            backend/bandit-report.json
            frontend/npm-audit.json
```

### Test Execution Strategy

#### Branch Protection Rules
```
main branch:
- Require status checks to pass:
  ✓ backend-tests
  ✓ frontend-tests
  ✓ e2e-tests (for releases)
  ✓ security-scan
- Require code review
- Require linear history
- Include administrators
```

#### Test Environments

##### Development
- **Trigger**: Every commit to feature branches
- **Tests**: Lint + Unit tests + Integration tests
- **Database**: In-memory or test container
- **Duration**: 3-5 minutes

##### Staging
- **Trigger**: PR to main/develop
- **Tests**: Full suite including E2E
- **Database**: Staging database
- **Duration**: 10-15 minutes

##### Production
- **Trigger**: Release tag
- **Tests**: Smoke tests only
- **Database**: Production (read-only tests)
- **Duration**: 2-3 minutes

### Deployment Pipeline

```
┌─────────────┐
│   Feature   │
│   Branch    │
└──────┬──────┘
       │ Push
       ▼
┌─────────────┐
│  Run Tests  │  ← Unit + Integration
└──────┬──────┘
       │ Success
       ▼
┌─────────────┐
│  Create PR  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Full Suite  │  ← All tests + E2E
└──────┬──────┘
       │ Success
       ▼
┌─────────────┐
│   Review    │
└──────┬──────┘
       │ Approved
       ▼
┌─────────────┐
│    Merge    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Deploy    │  ← Staging first
│   Staging   │
└──────┬──────┘
       │ QA Approval
       ▼
┌─────────────┐
│   Deploy    │
│  Production │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Smoke Tests  │
└─────────────┘
```

---

## Reporting and Metrics

### Test Reports

#### Daily Test Report
```markdown
# Daily Test Report - 2025-11-15

## Summary
- Tests Run: 850
- Passed: 845
- Failed: 3
- Flaky: 2
- Duration: 8m 34s

## Failed Tests
1. test_habit_streak_with_timezone - Investigation needed
2. test_export_csv_large_dataset - Timeout issue
3. test_goal_filter_by_category - UI regression

## Coverage
- Backend: 83.2% (+0.5% from yesterday)
- Frontend: 76.8% (+1.2% from yesterday)

## Action Items
- Fix timezone handling in habit tests
- Optimize CSV export for large datasets
- Investigate UI filtering regression
```

#### Weekly QA Report
```markdown
# Weekly QA Report - Week 46, 2025

## Testing Activity
- Test Cases Created: 45
- Test Cases Executed: 520
- Bugs Found: 12
- Bugs Fixed: 15
- Bugs Remaining: 8

## Quality Metrics
- Test Automation Rate: 78% (+3% from last week)
- Pass Rate: 96.2% (+1.1% from last week)
- Average Resolution Time: 2.3 days (-0.5 days improvement)

## Risk Areas
- Performance degradation in analytics module
- Intermittent failures in notification tests

## Achievements
- Completed E2E test suite for habits module
- Improved test execution time by 15%
- Zero critical bugs in production

## Next Week Plan
- Focus on performance testing
- Increase frontend coverage to 80%
- Implement visual regression testing
```

### Coverage Reports

#### Code Coverage Dashboard
```
Backend Coverage (Target: 80%)
┌────────────────────────┬──────────┬──────────┐
│ Module                 │ Coverage │ Status   │
├────────────────────────┼──────────┼──────────┤
│ api/endpoints          │ 92%      │ ✅       │
│ models                 │ 88%      │ ✅       │
│ services               │ 85%      │ ✅       │
│ utils                  │ 76%      │ ⚠️       │
│ core                   │ 81%      │ ✅       │
├────────────────────────┼──────────┼──────────┤
│ Overall                │ 83%      │ ✅       │
└────────────────────────┴──────────┴──────────┘

Frontend Coverage (Target: 75%)
┌────────────────────────┬──────────┬──────────┐
│ Module                 │ Coverage │ Status   │
├────────────────────────┼──────────┼──────────┤
│ components             │ 78%      │ ✅       │
│ pages                  │ 72%      │ ⚠️       │
│ services               │ 91%      │ ✅       │
│ hooks                  │ 85%      │ ✅       │
│ utils                  │ 88%      │ ✅       │
├────────────────────────┼──────────┼──────────┤
│ Overall                │ 77%      │ ✅       │
└────────────────────────┴──────────┴──────────┘
```

### Performance Metrics

#### API Performance
```
Endpoint Performance (95th percentile)
┌────────────────────────────────┬──────────┬──────────┐
│ Endpoint                       │ Response │ Target   │
├────────────────────────────────┼──────────┼──────────┤
│ POST /api/v1/auth/login        │ 145ms    │ <200ms ✅│
│ GET /api/v1/goals              │ 89ms     │ <100ms ✅│
│ POST /api/v1/goals             │ 112ms    │ <150ms ✅│
│ GET /api/v1/habits/{id}/entries│ 234ms    │ <300ms ✅│
│ POST /api/v1/workouts          │ 187ms    │ <200ms ✅│
│ GET /api/v1/analytics/dashboard│ 456ms    │ <500ms ✅│
└────────────────────────────────┴──────────┴──────────┘
```

#### Frontend Performance
```
Page Load Times (Lighthouse Scores)
┌─────────────────┬───────┬──────────────┬──────────┐
│ Page            │ Score │ FCP          │ LCP      │
├─────────────────┼───────┼──────────────┼──────────┤
│ Login           │ 98    │ 0.8s         │ 1.2s     │
│ Dashboard       │ 94    │ 1.1s         │ 1.8s     │
│ Goals List      │ 96    │ 0.9s         │ 1.4s     │
│ Goal Detail     │ 95    │ 1.0s         │ 1.6s     │
└─────────────────┴───────┴──────────────┴──────────┘
```

### Defect Analytics

#### Defect Distribution
```
By Severity:
┌──────────┬───────┬────────────┐
│ Severity │ Count │ Percentage │
├──────────┼───────┼────────────┤
│ Critical │ 0     │ 0%         │
│ High     │ 2     │ 16.7%      │
│ Medium   │ 6     │ 50.0%      │
│ Low      │ 4     │ 33.3%      │
└──────────┴───────┴────────────┘

By Module:
┌─────────────────┬───────┬────────────┐
│ Module          │ Count │ Percentage │
├─────────────────┼───────┼────────────┤
│ Goals           │ 4     │ 33.3%      │
│ Habits          │ 3     │ 25.0%      │
│ Authentication  │ 2     │ 16.7%      │
│ Dashboard       │ 2     │ 16.7%      │
│ Blog            │ 1     │ 8.3%       │
└─────────────────┴───────┴────────────┘
```

---

## Appendix

### Test Data Management

#### Test User Accounts
```python
# Predefined test users
TEST_USERS = {
    "basic_user": {
        "email": "test.user@example.com",
        "username": "testuser",
        "password": "TestPass123!"
    },
    "premium_user": {
        "email": "premium@example.com",
        "username": "premiumuser",
        "password": "PremiumPass123!"
    },
    "admin_user": {
        "email": "admin@example.com",
        "username": "adminuser",
        "password": "AdminPass123!"
    }
}
```

#### Test Data Factories
```python
# Using Faker for realistic test data
from faker import Faker

fake = Faker()

def create_test_goal(**kwargs):
    return {
        "title": kwargs.get("title", fake.sentence(nb_words=3)),
        "description": kwargs.get("description", fake.paragraph()),
        "goal_type": kwargs.get("goal_type", "yearly"),
        "category": kwargs.get("category", "personal"),
        "target_value": kwargs.get("target_value", fake.random_int(1, 100)),
        "target_unit": kwargs.get("target_unit", "units"),
        "start_date": kwargs.get("start_date", fake.date_this_year()),
        "end_date": kwargs.get("end_date", fake.date_this_year(after_today=True)),
        "priority": kwargs.get("priority", fake.random_int(1, 5))
    }
```

### Glossary

- **Acceptance Criteria**: Conditions that must be met for a feature to be accepted
- **Coverage**: Percentage of code executed by tests
- **E2E**: End-to-End, testing complete user workflows
- **Flaky Test**: Test that sometimes passes and sometimes fails without code changes
- **Integration Test**: Test that verifies multiple components work together
- **Regression**: Bug that was previously fixed but reappeared
- **Smoke Test**: Quick test of critical functionality
- **TDD**: Test-Driven Development, writing tests before implementation
- **Unit Test**: Test of a single function or component in isolation

### Resources

#### Documentation
- [Backend Testing Guide](backend/TESTING.md)
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)

#### Tools
- [Codecov](https://about.codecov.io/) - Coverage reporting
- [GitHub Actions](https://github.com/features/actions) - CI/CD
- [TestRail](https://www.gurock.com/testrail/) - Test management (optional)
- [Postman](https://www.postman.com/) - API testing

---

## Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-15 | 1.0.0 | Initial QA/Testing Plan | QA Team |

---

**Document Status**: ✅ Approved  
**Next Review Date**: 2025-12-15  
**Owner**: QA Team Lead  
**Contact**: qa@letsmanifest.com
