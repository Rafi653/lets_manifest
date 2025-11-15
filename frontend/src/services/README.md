# Services

This directory contains service layer implementations that encapsulate business logic and API interactions.

## Purpose

Services provide a clean abstraction layer between components and API calls, making it easier to:
- Manage complex data operations
- Reuse common logic across components
- Test business logic independently
- Handle error scenarios consistently

## Structure

Each service typically handles operations for a specific domain:
- `authService.ts` - Authentication and authorization
- `goalService.ts` - Goals management
- `habitService.ts` - Habits tracking
- `foodService.ts` - Food/nutrition tracking
- `workoutService.ts` - Workout tracking
- `reviewService.ts` - Daily reviews
- `blogService.ts` - Blog entries
- `progressService.ts` - Progress tracking

## Example

```typescript
// services/goalService.ts
import api from '../api/client';

export const goalService = {
  async getGoals() {
    const response = await api.get('/goals');
    return response.data;
  },
  
  async createGoal(goalData) {
    const response = await api.post('/goals', goalData);
    return response.data;
  }
};
```
