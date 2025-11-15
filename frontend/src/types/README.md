# TypeScript Types

This directory contains TypeScript type definitions and interfaces used throughout the application.

## Purpose

Centralized type definitions ensure:
- Type safety across the application
- Clear data contracts with the backend
- Better IDE support and autocompletion
- Easier refactoring

## Structure

- `api.types.ts` - API request/response types
- `auth.types.ts` - Authentication related types
- `goal.types.ts` - Goal domain types
- `habit.types.ts` - Habit domain types
- `food.types.ts` - Food/nutrition types
- `workout.types.ts` - Workout types
- `review.types.ts` - Daily review types
- `blog.types.ts` - Blog entry types
- `common.types.ts` - Common/shared types

## Example

```typescript
// types/goal.types.ts
export interface Goal {
  id: string;
  userId: string;
  title: string;
  description: string;
  goalType: 'short-term' | 'long-term' | 'habit';
  targetValue?: number;
  currentValue?: number;
  startDate: string;
  endDate?: string;
  status: 'active' | 'completed' | 'paused';
  createdAt: string;
  updatedAt: string;
}

export interface CreateGoalDTO {
  title: string;
  description: string;
  goalType: Goal['goalType'];
  targetValue?: number;
  startDate: string;
  endDate?: string;
}
```
