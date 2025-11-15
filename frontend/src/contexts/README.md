# React Contexts

This directory contains React Context providers for global state management.

## Purpose

React Context helps manage:
- Global application state
- User authentication state
- Theme preferences
- Notification system
- Other cross-cutting concerns

## Structure

- `AuthContext.tsx` - Authentication state and methods
- `ThemeContext.tsx` - Theme preferences (light/dark mode)
- `NotificationContext.tsx` - App-wide notifications/toasts

## Example

```typescript
// contexts/AuthContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface AuthContextType {
  user: User | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  // Implementation here

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```
