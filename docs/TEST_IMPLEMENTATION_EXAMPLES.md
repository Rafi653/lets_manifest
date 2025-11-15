# Test Implementation Examples

This document provides practical examples of test implementations for Let's Manifest using the recommended testing frameworks.

---

## Backend Test Examples (Python + pytest)

### 1. Unit Test Example - Service Layer

```python
# tests/unit/test_goal_service.py
import pytest
from datetime import date, timedelta
from app.services.goal_service import GoalService
from app.models.goal import Goal

class TestGoalService:
    """Unit tests for Goal Service"""
    
    def test_calculate_completion_percentage_within_target(self):
        """Test completion percentage calculation when progress is within target"""
        # Arrange
        goal = Goal(
            title="Run 100 miles",
            target_value=100.0,
            current_value=0.0
        )
        progress_value = 50.0
        
        # Act
        result = GoalService.calculate_completion_percentage(goal, progress_value)
        
        # Assert
        assert result == 50.0
    
    def test_calculate_completion_percentage_exceeds_target(self):
        """Test completion percentage is capped at 100% when progress exceeds target"""
        # Arrange
        goal = Goal(
            title="Run 100 miles",
            target_value=100.0,
            current_value=0.0
        )
        progress_value = 150.0
        
        # Act
        result = GoalService.calculate_completion_percentage(goal, progress_value)
        
        # Assert
        assert result == 100.0
    
    def test_calculate_completion_percentage_zero_target(self):
        """Test completion percentage with zero target value"""
        # Arrange
        goal = Goal(
            title="Complete tasks",
            target_value=0.0,
            current_value=0.0
        )
        progress_value = 10.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Target value cannot be zero"):
            GoalService.calculate_completion_percentage(goal, progress_value)
    
    def test_is_goal_overdue_returns_true_for_past_deadline(self):
        """Test that overdue detection works for past end dates"""
        # Arrange
        goal = Goal(
            title="Past goal",
            end_date=date.today() - timedelta(days=1)
        )
        
        # Act
        result = GoalService.is_goal_overdue(goal)
        
        # Assert
        assert result is True
    
    def test_is_goal_overdue_returns_false_for_future_deadline(self):
        """Test that overdue detection works for future end dates"""
        # Arrange
        goal = Goal(
            title="Future goal",
            end_date=date.today() + timedelta(days=7)
        )
        
        # Act
        result = GoalService.is_goal_overdue(goal)
        
        # Assert
        assert result is False
```

### 2. Integration Test Example - API with Database

```python
# tests/integration/test_goal_api.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.models.goal import Goal
from app.core.deps import get_db
from tests.conftest import override_get_db, get_test_db

@pytest.mark.asyncio
class TestGoalAPI:
    """Integration tests for Goal API endpoints"""
    
    async def test_create_goal_success(
        self,
        async_client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession
    ):
        """Test successful goal creation via API"""
        # Arrange
        goal_data = {
            "title": "Complete Marathon",
            "description": "Run a full marathon in under 4 hours",
            "goal_type": "yearly",
            "category": "fitness",
            "target_value": 42.195,
            "target_unit": "km",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "priority": 5
        }
        
        # Act
        response = await async_client.post(
            "/api/v1/goals",
            json=goal_data,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Goal created successfully"
        assert data["data"]["title"] == goal_data["title"]
        assert data["data"]["target_value"] == goal_data["target_value"]
        
        # Verify in database
        goal_id = data["data"]["id"]
        result = await db_session.execute(
            "SELECT * FROM goals WHERE id = :id",
            {"id": goal_id}
        )
        db_goal = result.fetchone()
        assert db_goal is not None
        assert db_goal.title == goal_data["title"]
    
    async def test_create_goal_validation_error(
        self,
        async_client: AsyncClient,
        auth_headers: dict
    ):
        """Test goal creation with invalid data"""
        # Arrange
        invalid_goal = {
            "title": "",  # Empty title should fail validation
            "goal_type": "invalid_type",  # Invalid type
            "target_value": -10  # Negative value should fail
        }
        
        # Act
        response = await async_client.post(
            "/api/v1/goals",
            json=invalid_goal,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "errors" in data
        assert len(data["errors"]) > 0
    
    async def test_get_goals_with_pagination(
        self,
        async_client: AsyncClient,
        auth_headers: dict,
        seed_goals
    ):
        """Test retrieving goals with pagination"""
        # Act
        response = await async_client.get(
            "/api/v1/goals?page=1&limit=10",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert "page" in data["data"]
        assert data["data"]["page"] == 1
        assert len(data["data"]["items"]) <= 10
    
    async def test_update_goal_success(
        self,
        async_client: AsyncClient,
        auth_headers: dict,
        test_goal
    ):
        """Test successful goal update"""
        # Arrange
        update_data = {
            "title": "Updated Marathon Goal",
            "target_value": 50.0
        }
        
        # Act
        response = await async_client.put(
            f"/api/v1/goals/{test_goal.id}",
            json=update_data,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == update_data["title"]
        assert data["data"]["target_value"] == update_data["target_value"]
    
    async def test_delete_goal_success(
        self,
        async_client: AsyncClient,
        auth_headers: dict,
        test_goal,
        db_session: AsyncSession
    ):
        """Test successful goal deletion"""
        # Act
        response = await async_client.delete(
            f"/api/v1/goals/{test_goal.id}",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify deletion in database
        result = await db_session.execute(
            "SELECT * FROM goals WHERE id = :id",
            {"id": test_goal.id}
        )
        db_goal = result.fetchone()
        assert db_goal is None
    
    async def test_add_progress_entry(
        self,
        async_client: AsyncClient,
        auth_headers: dict,
        test_goal
    ):
        """Test adding progress entry to goal"""
        # Arrange
        progress_data = {
            "date": "2025-11-15",
            "value": 25.0,
            "notes": "Completed week 1 of training"
        }
        
        # Act
        response = await async_client.post(
            f"/api/v1/goals/{test_goal.id}/progress",
            json=progress_data,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["value"] == progress_data["value"]
        assert data["data"]["notes"] == progress_data["notes"]
```

### 3. Authentication Test Example

```python
# tests/integration/test_auth_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestAuthAPI:
    """Integration tests for Authentication endpoints"""
    
    async def test_register_user_success(self, async_client: AsyncClient):
        """Test successful user registration"""
        # Arrange
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "SecurePass123!",
            "first_name": "New",
            "last_name": "User"
        }
        
        # Act
        response = await async_client.post(
            "/api/v1/auth/register",
            json=user_data
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["email"] == user_data["email"]
        assert data["data"]["username"] == user_data["username"]
        assert "password" not in data["data"]  # Password should not be returned
    
    async def test_register_duplicate_email(
        self,
        async_client: AsyncClient,
        existing_user
    ):
        """Test registration with duplicate email fails"""
        # Arrange
        user_data = {
            "email": existing_user.email,  # Duplicate email
            "username": "differentuser",
            "password": "SecurePass123!"
        }
        
        # Act
        response = await async_client.post(
            "/api/v1/auth/register",
            json=user_data
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "email" in data["message"].lower()
    
    async def test_login_success(self, async_client: AsyncClient, existing_user):
        """Test successful login"""
        # Arrange
        credentials = {
            "email": existing_user.email,
            "password": "password123"  # Assuming this is the test password
        }
        
        # Act
        response = await async_client.post(
            "/api/v1/auth/login",
            json=credentials
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["data"]
        assert "token_type" in data["data"]
        assert data["data"]["token_type"] == "bearer"
    
    async def test_login_invalid_credentials(self, async_client: AsyncClient):
        """Test login with invalid credentials"""
        # Arrange
        credentials = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        # Act
        response = await async_client.post(
            "/api/v1/auth/login",
            json=credentials
        )
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "invalid" in data["message"].lower()
    
    async def test_protected_endpoint_without_token(
        self,
        async_client: AsyncClient
    ):
        """Test accessing protected endpoint without token"""
        # Act
        response = await async_client.get("/api/v1/users/me")
        
        # Assert
        assert response.status_code == 401
    
    async def test_protected_endpoint_with_valid_token(
        self,
        async_client: AsyncClient,
        auth_headers: dict
    ):
        """Test accessing protected endpoint with valid token"""
        # Act
        response = await async_client.get(
            "/api/v1/users/me",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "email" in data["data"]
        assert "username" in data["data"]
```

---

## Frontend Test Examples (React + Vitest + Testing Library)

### 1. Component Unit Test Example

```typescript
// src/components/GoalCard.test.tsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import userEvent from '@testing-library/user-event'
import { GoalCard } from './GoalCard'

describe('GoalCard', () => {
  const mockGoal = {
    id: '1',
    title: 'Complete Marathon',
    description: 'Run a full marathon',
    goalType: 'yearly',
    category: 'fitness',
    targetValue: 42.195,
    targetUnit: 'km',
    currentValue: 21.0,
    completionPercentage: 50,
    startDate: '2025-01-01',
    endDate: '2025-12-31',
    priority: 5,
    status: 'active'
  }

  it('renders goal title and description', () => {
    render(<GoalCard goal={mockGoal} />)
    
    expect(screen.getByText('Complete Marathon')).toBeInTheDocument()
    expect(screen.getByText('Run a full marathon')).toBeInTheDocument()
  })

  it('displays correct completion percentage', () => {
    render(<GoalCard goal={mockGoal} />)
    
    expect(screen.getByText('50%')).toBeInTheDocument()
  })

  it('shows progress bar with correct width', () => {
    render(<GoalCard goal={mockGoal} />)
    
    const progressBar = screen.getByRole('progressbar')
    expect(progressBar).toHaveAttribute('aria-valuenow', '50')
  })

  it('calls onEdit when edit button is clicked', async () => {
    const user = userEvent.setup()
    const onEdit = vi.fn()
    
    render(<GoalCard goal={mockGoal} onEdit={onEdit} />)
    
    const editButton = screen.getByRole('button', { name: /edit/i })
    await user.click(editButton)
    
    expect(onEdit).toHaveBeenCalledWith(mockGoal.id)
  })

  it('calls onDelete when delete button is clicked', async () => {
    const user = userEvent.setup()
    const onDelete = vi.fn()
    
    render(<GoalCard goal={mockGoal} onDelete={onDelete} />)
    
    const deleteButton = screen.getByRole('button', { name: /delete/i })
    await user.click(deleteButton)
    
    expect(onDelete).toHaveBeenCalledWith(mockGoal.id)
  })

  it('displays goal category badge', () => {
    render(<GoalCard goal={mockGoal} />)
    
    expect(screen.getByText('fitness')).toBeInTheDocument()
  })

  it('shows overdue indicator when past end date', () => {
    const overdueGoal = {
      ...mockGoal,
      endDate: '2024-12-31' // Past date
    }
    
    render(<GoalCard goal={overdueGoal} />)
    
    expect(screen.getByText(/overdue/i)).toBeInTheDocument()
  })

  it('applies correct styling based on priority', () => {
    const { container } = render(<GoalCard goal={mockGoal} />)
    
    const card = container.firstChild
    expect(card).toHaveClass('priority-5')
  })
})
```

### 2. Form Component Test Example

```typescript
// src/components/GoalForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import userEvent from '@testing-library/user-event'
import { GoalForm } from './GoalForm'

describe('GoalForm', () => {
  const mockOnSubmit = vi.fn()
  const mockOnCancel = vi.fn()

  beforeEach(() => {
    mockOnSubmit.mockClear()
    mockOnCancel.mockClear()
  })

  it('renders all form fields', () => {
    render(<GoalForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)
    
    expect(screen.getByLabelText(/title/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/goal type/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/category/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/target value/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/start date/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/end date/i)).toBeInTheDocument()
  })

  it('validates required fields on submit', async () => {
    const user = userEvent.setup()
    render(<GoalForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)
    
    const submitButton = screen.getByRole('button', { name: /create goal/i })
    await user.click(submitButton)
    
    expect(await screen.findByText(/title is required/i)).toBeInTheDocument()
    expect(mockOnSubmit).not.toHaveBeenCalled()
  })

  it('validates target value is positive', async () => {
    const user = userEvent.setup()
    render(<GoalForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)
    
    const targetInput = screen.getByLabelText(/target value/i)
    await user.type(targetInput, '-10')
    
    await user.click(screen.getByRole('button', { name: /create goal/i }))
    
    expect(
      await screen.findByText(/target value must be positive/i)
    ).toBeInTheDocument()
  })

  it('validates end date is after start date', async () => {
    const user = userEvent.setup()
    render(<GoalForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)
    
    const startDateInput = screen.getByLabelText(/start date/i)
    const endDateInput = screen.getByLabelText(/end date/i)
    
    await user.type(startDateInput, '2025-12-31')
    await user.type(endDateInput, '2025-01-01')
    
    await user.click(screen.getByRole('button', { name: /create goal/i }))
    
    expect(
      await screen.findByText(/end date must be after start date/i)
    ).toBeInTheDocument()
  })

  it('submits form with valid data', async () => {
    const user = userEvent.setup()
    render(<GoalForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)
    
    // Fill in all fields
    await user.type(screen.getByLabelText(/title/i), 'New Goal')
    await user.type(
      screen.getByLabelText(/description/i),
      'Goal description'
    )
    await user.selectOptions(screen.getByLabelText(/goal type/i), 'yearly')
    await user.selectOptions(screen.getByLabelText(/category/i), 'fitness')
    await user.type(screen.getByLabelText(/target value/i), '100')
    await user.type(screen.getByLabelText(/target unit/i), 'km')
    await user.type(screen.getByLabelText(/start date/i), '2025-01-01')
    await user.type(screen.getByLabelText(/end date/i), '2025-12-31')
    
    await user.click(screen.getByRole('button', { name: /create goal/i }))
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        title: 'New Goal',
        description: 'Goal description',
        goalType: 'yearly',
        category: 'fitness',
        targetValue: 100,
        targetUnit: 'km',
        startDate: '2025-01-01',
        endDate: '2025-12-31'
      })
    })
  })

  it('calls onCancel when cancel button is clicked', async () => {
    const user = userEvent.setup()
    render(<GoalForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />)
    
    const cancelButton = screen.getByRole('button', { name: /cancel/i })
    await user.click(cancelButton)
    
    expect(mockOnCancel).toHaveBeenCalled()
  })

  it('populates form with initial data in edit mode', () => {
    const initialData = {
      id: '1',
      title: 'Existing Goal',
      description: 'Existing description',
      goalType: 'monthly',
      category: 'personal',
      targetValue: 50,
      targetUnit: 'hours',
      startDate: '2025-01-01',
      endDate: '2025-01-31'
    }
    
    render(
      <GoalForm
        initialData={initialData}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )
    
    expect(screen.getByLabelText(/title/i)).toHaveValue('Existing Goal')
    expect(screen.getByLabelText(/description/i)).toHaveValue(
      'Existing description'
    )
    expect(screen.getByLabelText(/goal type/i)).toHaveValue('monthly')
    expect(screen.getByLabelText(/target value/i)).toHaveValue(50)
  })
})
```

### 3. API Service Test Example with MSW

```typescript
// src/services/goalService.test.ts
import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'
import { goalService } from './goalService'

const server = setupServer()

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('GoalService', () => {
  describe('getGoals', () => {
    it('fetches goals successfully', async () => {
      const mockGoals = [
        { id: '1', title: 'Goal 1', targetValue: 100 },
        { id: '2', title: 'Goal 2', targetValue: 200 }
      ]

      server.use(
        http.get('/api/v1/goals', () => {
          return HttpResponse.json({
            data: { items: mockGoals, total: 2 }
          })
        })
      )

      const result = await goalService.getGoals()

      expect(result.items).toHaveLength(2)
      expect(result.items[0].title).toBe('Goal 1')
    })

    it('handles API error', async () => {
      server.use(
        http.get('/api/v1/goals', () => {
          return HttpResponse.json(
            { message: 'Server error' },
            { status: 500 }
          )
        })
      )

      await expect(goalService.getGoals()).rejects.toThrow()
    })

    it('sends correct query parameters', async () => {
      let capturedParams: URLSearchParams | null = null

      server.use(
        http.get('/api/v1/goals', ({ request }) => {
          capturedParams = new URL(request.url).searchParams
          return HttpResponse.json({ data: { items: [], total: 0 } })
        })
      )

      await goalService.getGoals({ page: 2, limit: 20, goalType: 'yearly' })

      expect(capturedParams?.get('page')).toBe('2')
      expect(capturedParams?.get('limit')).toBe('20')
      expect(capturedParams?.get('goalType')).toBe('yearly')
    })
  })

  describe('createGoal', () => {
    it('creates goal successfully', async () => {
      const newGoal = {
        title: 'New Goal',
        goalType: 'yearly',
        targetValue: 100
      }

      const createdGoal = { id: '123', ...newGoal }

      server.use(
        http.post('/api/v1/goals', async ({ request }) => {
          const body = await request.json()
          return HttpResponse.json(
            { data: { ...body, id: '123' } },
            { status: 201 }
          )
        })
      )

      const result = await goalService.createGoal(newGoal)

      expect(result.id).toBe('123')
      expect(result.title).toBe(newGoal.title)
    })

    it('handles validation error', async () => {
      server.use(
        http.post('/api/v1/goals', () => {
          return HttpResponse.json(
            {
              message: 'Validation error',
              errors: [{ field: 'title', message: 'Title is required' }]
            },
            { status: 422 }
          )
        })
      )

      await expect(
        goalService.createGoal({ title: '', goalType: 'yearly' })
      ).rejects.toThrow()
    })
  })

  describe('updateGoal', () => {
    it('updates goal successfully', async () => {
      const updates = { title: 'Updated Title' }

      server.use(
        http.put('/api/v1/goals/:id', async ({ params, request }) => {
          const body = await request.json()
          return HttpResponse.json({
            data: { id: params.id, ...body }
          })
        })
      )

      const result = await goalService.updateGoal('123', updates)

      expect(result.title).toBe('Updated Title')
    })
  })

  describe('deleteGoal', () => {
    it('deletes goal successfully', async () => {
      server.use(
        http.delete('/api/v1/goals/:id', () => {
          return HttpResponse.json(
            { message: 'Goal deleted successfully' },
            { status: 200 }
          )
        })
      )

      await expect(goalService.deleteGoal('123')).resolves.not.toThrow()
    })
  })
})
```

### 4. Custom Hook Test Example

```typescript
// src/hooks/useGoals.test.ts
import { renderHook, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useGoals } from './useGoals'
import { goalService } from '../services/goalService'

vi.mock('../services/goalService')

describe('useGoals', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetches goals on mount', async () => {
    const mockGoals = [
      { id: '1', title: 'Goal 1' },
      { id: '2', title: 'Goal 2' }
    ]

    vi.mocked(goalService.getGoals).mockResolvedValue({
      items: mockGoals,
      total: 2
    })

    const { result } = renderHook(() => useGoals())

    expect(result.current.loading).toBe(true)

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.goals).toEqual(mockGoals)
    expect(goalService.getGoals).toHaveBeenCalledOnce()
  })

  it('handles fetch error', async () => {
    const error = new Error('Failed to fetch')
    vi.mocked(goalService.getGoals).mockRejectedValue(error)

    const { result } = renderHook(() => useGoals())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.error).toBe(error)
    expect(result.current.goals).toEqual([])
  })

  it('creates goal successfully', async () => {
    const newGoal = { title: 'New Goal', goalType: 'yearly' }
    const createdGoal = { id: '123', ...newGoal }

    vi.mocked(goalService.getGoals).mockResolvedValue({
      items: [],
      total: 0
    })
    vi.mocked(goalService.createGoal).mockResolvedValue(createdGoal)

    const { result } = renderHook(() => useGoals())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    const createResult = await result.current.createGoal(newGoal)

    expect(createResult).toEqual(createdGoal)
    expect(goalService.createGoal).toHaveBeenCalledWith(newGoal)
  })

  it('refreshes goals after creation', async () => {
    const newGoal = { title: 'New Goal', goalType: 'yearly' }
    const createdGoal = { id: '123', ...newGoal }

    vi.mocked(goalService.getGoals).mockResolvedValue({
      items: [],
      total: 0
    })
    vi.mocked(goalService.createGoal).mockResolvedValue(createdGoal)

    const { result } = renderHook(() => useGoals())

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    await result.current.createGoal(newGoal)

    // Verify getGoals was called again (initial + after create)
    expect(goalService.getGoals).toHaveBeenCalledTimes(2)
  })
})
```

---

## E2E Test Examples (Playwright)

### 1. Authentication Flow E2E Test

```typescript
// e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test'

test.describe('User Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173')
  })

  test('user can register and login', async ({ page }) => {
    // Navigate to registration
    await page.click('text=Sign Up')
    
    // Fill registration form
    await page.fill('[name="email"]', 'testuser@example.com')
    await page.fill('[name="username"]', 'testuser')
    await page.fill('[name="password"]', 'SecurePass123!')
    await page.fill('[name="confirmPassword"]', 'SecurePass123!')
    await page.fill('[name="firstName"]', 'Test')
    await page.fill('[name="lastName"]', 'User')
    
    // Submit registration
    await page.click('button:has-text("Register")')
    
    // Should redirect to login
    await expect(page).toHaveURL(/.*login/)
    await expect(page.locator('text=Registration successful')).toBeVisible()
    
    // Login with new credentials
    await page.fill('[name="email"]', 'testuser@example.com')
    await page.fill('[name="password"]', 'SecurePass123!')
    await page.click('button:has-text("Login")')
    
    // Should reach dashboard
    await expect(page).toHaveURL(/.*dashboard/)
    await expect(page.locator('h1:has-text("Dashboard")')).toBeVisible()
  })

  test('login with invalid credentials shows error', async ({ page }) => {
    await page.click('text=Login')
    
    await page.fill('[name="email"]', 'invalid@example.com')
    await page.fill('[name="password"]', 'wrongpassword')
    await page.click('button:has-text("Login")')
    
    await expect(
      page.locator('text=Invalid email or password')
    ).toBeVisible()
    await expect(page).not.toHaveURL(/.*dashboard/)
  })

  test('protected routes redirect to login', async ({ page }) => {
    await page.goto('http://localhost:5173/dashboard')
    
    // Should redirect to login
    await expect(page).toHaveURL(/.*login/)
  })

  test('user can logout', async ({ page }) => {
    // Login first
    await page.click('text=Login')
    await page.fill('[name="email"]', 'testuser@example.com')
    await page.fill('[name="password"]', 'SecurePass123!')
    await page.click('button:has-text("Login")')
    
    await expect(page).toHaveURL(/.*dashboard/)
    
    // Logout
    await page.click('[data-testid="user-menu"]')
    await page.click('text=Logout')
    
    // Should redirect to home
    await expect(page).toHaveURL(/.*\/\s*$/)
    
    // Dashboard should not be accessible
    await page.goto('http://localhost:5173/dashboard')
    await expect(page).toHaveURL(/.*login/)
  })
})
```

### 2. Goal Management E2E Test

```typescript
// e2e/goals/goal-management.spec.ts
import { test, expect } from '@playwright/test'
import { loginAsUser } from '../helpers/auth'

test.describe('Goal Management', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsUser(page, {
      email: 'testuser@example.com',
      password: 'SecurePass123!'
    })
  })

  test('user can create a new goal', async ({ page }) => {
    // Navigate to goals
    await page.click('nav >> text=Goals')
    await expect(page).toHaveURL(/.*goals/)
    
    // Click new goal button
    await page.click('button:has-text("New Goal")')
    
    // Fill goal form
    await page.fill('[name="title"]', 'Run 100 miles')
    await page.fill('[name="description"]', 'Run 100 miles this year')
    await page.selectOption('[name="goalType"]', 'yearly')
    await page.selectOption('[name="category"]', 'fitness')
    await page.fill('[name="targetValue"]', '100')
    await page.fill('[name="targetUnit"]', 'miles')
    await page.fill('[name="startDate"]', '2025-01-01')
    await page.fill('[name="endDate"]', '2025-12-31')
    await page.fill('[name="priority"]', '5')
    
    // Submit form
    await page.click('button:has-text("Create Goal")')
    
    // Verify goal appears in list
    await expect(page.locator('text=Run 100 miles')).toBeVisible()
    await expect(page.locator('text=0%')).toBeVisible() // Initial progress
  })

  test('user can add progress to a goal', async ({ page }) => {
    await page.click('nav >> text=Goals')
    
    // Click on a goal
    await page.click('text=Run 100 miles')
    
    // Add progress
    await page.click('button:has-text("Add Progress")')
    await page.fill('[name="value"]', '25')
    await page.fill('[name="notes"]', 'Completed week 1')
    await page.click('button:has-text("Save Progress")')
    
    // Verify progress updated
    await expect(page.locator('text=25%')).toBeVisible()
    await expect(page.locator('text=Completed week 1')).toBeVisible()
  })

  test('user can filter goals by type', async ({ page }) => {
    await page.click('nav >> text=Goals')
    
    // Apply filter
    await page.selectOption('[name="goalTypeFilter"]', 'yearly')
    
    // Verify only yearly goals shown
    const goals = page.locator('[data-testid^="goal-card-"]')
    await expect(goals).toHaveCount(await goals.count())
    
    for (const goal of await goals.all()) {
      await expect(goal.locator('[data-testid="goal-type"]')).toHaveText(
        'yearly'
      )
    }
  })

  test('user can edit a goal', async ({ page }) => {
    await page.click('nav >> text=Goals')
    await page.click('text=Run 100 miles')
    
    // Click edit
    await page.click('button:has-text("Edit")')
    
    // Update title
    await page.fill('[name="title"]', 'Run 150 miles')
    await page.fill('[name="targetValue"]', '150')
    await page.click('button:has-text("Save Changes")')
    
    // Verify updates
    await expect(page.locator('text=Run 150 miles')).toBeVisible()
  })

  test('user can delete a goal', async ({ page }) => {
    await page.click('nav >> text=Goals')
    await page.click('text=Run 100 miles')
    
    // Delete goal
    await page.click('button:has-text("Delete")')
    
    // Confirm deletion
    await page.click('button:has-text("Confirm")')
    
    // Verify goal removed from list
    await expect(page.locator('text=Run 100 miles')).not.toBeVisible()
  })
})
```

### 3. Complete User Journey E2E Test

```typescript
// e2e/journey/complete-workflow.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Complete User Journey', () => {
  test('new user completes full onboarding and creates first goal', async ({
    page
  }) => {
    // 1. Register
    await page.goto('http://localhost:5173')
    await page.click('text=Sign Up')
    
    await page.fill('[name="email"]', `user${Date.now()}@example.com`)
    await page.fill('[name="username"]', `user${Date.now()}`)
    await page.fill('[name="password"]', 'SecurePass123!')
    await page.fill('[name="confirmPassword"]', 'SecurePass123!')
    await page.fill('[name="firstName"]', 'Test')
    await page.fill('[name="lastName"]', 'User')
    await page.click('button:has-text("Register")')
    
    // 2. Login
    await expect(page).toHaveURL(/.*login/)
    const email = await page.inputValue('[name="email"]')
    await page.fill('[name="password"]', 'SecurePass123!')
    await page.click('button:has-text("Login")')
    
    // 3. Welcome to Dashboard
    await expect(page).toHaveURL(/.*dashboard/)
    await expect(page.locator('text=Welcome')).toBeVisible()
    
    // 4. Create first goal
    await page.click('nav >> text=Goals')
    await page.click('button:has-text("New Goal")')
    await page.fill('[name="title"]', 'My First Goal')
    await page.selectOption('[name="goalType"]', 'monthly')
    await page.fill('[name="targetValue"]', '10')
    await page.click('button:has-text("Create Goal")')
    
    // 5. Verify goal created
    await expect(page.locator('text=My First Goal')).toBeVisible()
    
    // 6. Create a habit
    await page.click('nav >> text=Habits')
    await page.click('button:has-text("New Habit")')
    await page.fill('[name="name"]', 'Morning Exercise')
    await page.selectOption('[name="frequency"]', 'daily')
    await page.click('button:has-text("Create Habit")')
    
    // 7. Check in to habit
    await page.click('[data-testid="habit-checkin-Morning Exercise"]')
    await expect(page.locator('text=Streak: 1 day')).toBeVisible()
    
    // 8. View dashboard with data
    await page.click('nav >> text=Dashboard')
    await expect(page.locator('[data-testid="active-goals"]')).toContainText(
      '1'
    )
    await expect(page.locator('[data-testid="active-habits"]')).toContainText(
      '1'
    )
  })
})
```

---

## Test Fixtures and Helpers

### Backend Test Fixtures

```python
# tests/conftest.py
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.main import app
from app.core.config import settings
from app.models.user import User
from app.core.security import get_password_hash

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_session():
    """Provide test database session"""
    engine = create_async_engine(settings.TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture
async def async_client(db_session):
    """Provide async HTTP client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def test_user(db_session):
    """Create test user"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password123"),
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def auth_headers(test_user):
    """Provide authentication headers"""
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": test_user.id})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def test_goal(db_session, test_user):
    """Create test goal"""
    from app.models.goal import Goal
    goal = Goal(
        user_id=test_user.id,
        title="Test Goal",
        goal_type="yearly",
        category="fitness",
        target_value=100.0,
        target_unit="units"
    )
    db_session.add(goal)
    await db_session.commit()
    await db_session.refresh(goal)
    return goal
```

### Frontend Test Helpers

```typescript
// src/tests/helpers/auth.ts
import { Page } from '@playwright/test'

export async function loginAsUser(
  page: Page,
  credentials: { email: string; password: string }
) {
  await page.goto('http://localhost:5173/login')
  await page.fill('[name="email"]', credentials.email)
  await page.fill('[name="password"]', credentials.password)
  await page.click('button:has-text("Login")')
  await page.waitForURL('**/dashboard')
}

export async function setupAuthenticatedContext(page: Page) {
  await loginAsUser(page, {
    email: 'testuser@example.com',
    password: 'SecurePass123!'
  })
  
  // Save storage state for reuse
  await page.context().storageState({ path: 'auth.json' })
}
```

```typescript
// src/tests/setup.ts
import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom'

afterEach(() => {
  cleanup()
})
```

---

## Running Tests

### Backend
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific marker
pytest -m unit
pytest -m integration

# Run with verbose output
pytest -v -s

# Run specific file
pytest tests/unit/test_goal_service.py
```

### Frontend
```bash
# Run all tests
npm run test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch

# Run E2E tests
npm run test:e2e

# Run specific test file
npm run test -- src/components/GoalCard.test.tsx
```

---

This document provides a comprehensive set of test implementation examples that demonstrate best practices for testing the Let's Manifest application. Use these as templates when writing your own tests.
