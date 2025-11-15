# Custom Hooks

This directory contains custom React hooks for reusable logic across components.

## Purpose

Custom hooks help:
- Share stateful logic between components
- Keep components clean and focused
- Make code more testable
- Follow React best practices

## Common Hooks

- `useAuth.ts` - Authentication state and operations
- `useApi.ts` - Generic API call hook with loading/error states
- `useLocalStorage.ts` - Persist state in localStorage
- `useDebounce.ts` - Debounce values for performance
- `useForm.ts` - Form state management

## Example

```typescript
// hooks/useAuth.ts
import { useState, useEffect } from 'react';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Authentication logic here
  
  return { user, isLoading, login, logout };
};
```
