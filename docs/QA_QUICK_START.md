# QA/Testing Quick Start Guide

This is a quick reference guide to get started with QA and testing for Let's Manifest.

---

## 📋 Overview

Let's Manifest uses a comprehensive testing strategy covering:
- **Backend**: Python + pytest + httpx
- **Frontend**: React + Vitest + Testing Library (to be implemented)
- **E2E**: Playwright (to be implemented)
- **CI/CD**: GitHub Actions

---

## 🚀 Quick Start

### Backend Testing

#### Run Tests
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test types
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests only

# Run specific test file
pytest tests/unit/test_goal_service.py

# Run with verbose output
pytest -v
```

#### Test Structure
```
backend/tests/
├── conftest.py           # Shared fixtures
├── unit/                 # Unit tests
│   ├── test_*.py
│   └── ...
└── integration/          # Integration tests
    ├── test_*.py
    └── ...
```

### Frontend Testing (To Be Implemented)

#### Setup Testing Framework
```bash
cd frontend

# Install testing dependencies
npm install -D vitest @testing-library/react @testing-library/jest-dom \
  @testing-library/user-event jsdom @vitest/ui c8

# Install E2E testing
npm install -D @playwright/test
npx playwright install
```

#### Run Tests (Once Implemented)
```bash
cd frontend

# Run unit/component tests
npm run test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch

# Run E2E tests
npm run test:e2e
```

---

## 📚 Key Documents

1. **[QA_TESTING_PLAN.md](../QA_TESTING_PLAN.md)** - Main testing strategy document
2. **[TEST_CASE_TEMPLATES.md](TEST_CASE_TEMPLATES.md)** - Templates for writing test cases
3. **[TEST_IMPLEMENTATION_EXAMPLES.md](TEST_IMPLEMENTATION_EXAMPLES.md)** - Code examples
4. **[QA_TEST_TRACKING_CHECKLIST.md](QA_TEST_TRACKING_CHECKLIST.md)** - Progress tracking

---

## 🎯 Coverage Targets

| Component | Target | Critical Paths |
|-----------|--------|----------------|
| Backend Overall | 80% | 95% |
| Backend API Endpoints | 100% | 100% |
| Backend Models | 90% | 100% |
| Frontend Overall | 75% | 90% |
| Frontend Components | 75% | 90% |

---

## ✅ Test Types

### Unit Tests (55-70%)
- Test individual functions/components
- Fast execution (milliseconds)
- No external dependencies
- **Example**: Testing a calculation function

### Integration Tests (20-30%)
- Test multiple components together
- Medium speed (seconds)
- May involve database/API
- **Example**: Testing API endpoint with database

### E2E Tests (10-15%)
- Test complete user workflows
- Slower execution (seconds to minutes)
- Full application stack
- **Example**: Complete user registration to dashboard flow

---

## 🔧 Writing Tests

### Backend Test Example
```python
# tests/unit/test_goal_service.py
import pytest
from app.services.goal_service import GoalService

def test_calculate_completion_percentage():
    # Arrange
    target = 100.0
    current = 50.0
    
    # Act
    result = GoalService.calculate_completion_percentage(target, current)
    
    # Assert
    assert result == 50.0
```

### Frontend Test Example (Pattern)
```typescript
// src/components/GoalCard.test.tsx
import { render, screen } from '@testing-library/react'
import { GoalCard } from './GoalCard'

test('renders goal title', () => {
  const goal = { id: '1', title: 'Test Goal', targetValue: 100 }
  render(<GoalCard goal={goal} />)
  expect(screen.getByText('Test Goal')).toBeInTheDocument()
})
```

### E2E Test Example (Pattern)
```typescript
// e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test'

test('user can login', async ({ page }) => {
  await page.goto('http://localhost:5173/login')
  await page.fill('[name="email"]', 'user@example.com')
  await page.fill('[name="password"]', 'password')
  await page.click('button:has-text("Login")')
  await expect(page).toHaveURL(/.*dashboard/)
})
```

---

## 🔄 CI/CD Pipeline

### Automated Testing
The CI pipeline runs automatically on:
- Every push to `main` or `develop` branches
- Every pull request to `main` or `develop`

### Pipeline Steps
1. **Backend Linting** - Ruff + Black + mypy
2. **Backend Tests** - Unit + Integration with coverage
3. **Frontend Linting** - ESLint + TypeScript check
4. **Frontend Tests** - Unit + Component tests (when implemented)
5. **E2E Tests** - Critical user journeys (on PRs)
6. **Security Scan** - Bandit + npm audit
7. **Build** - Verify application builds successfully

### Viewing Results
- Check GitHub Actions tab for pipeline status
- Coverage reports uploaded to Codecov (when configured)
- Test artifacts available in GitHub Actions runs

---

## 🐛 Bug Reporting

### Bug Report Template
```markdown
## Summary
[Brief description]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Browser: [Chrome/Firefox/etc.]
- OS: [Windows/Mac/Linux]
- Version: [App version]

## Additional Info
[Screenshots, logs, etc.]
```

---

## 📊 Test Tracking

### For Each Sprint
1. Review test tracking checklist
2. Mark completed tests
3. Update coverage metrics
4. Document blockers and risks
5. Generate test summary report

### Key Metrics to Track
- Test execution rate (passed/total)
- Code coverage percentage
- Bug discovery rate
- Time to fix bugs
- Test automation percentage

---

## 👥 Roles and Responsibilities

### QA Engineer
- Define test strategy
- Write test cases
- Execute manual tests
- Report bugs
- Verify fixes
- Sign off on releases

### Developers
- Write unit and integration tests
- Fix failing tests
- Maintain test coverage
- Review test code

### Tech Lead
- Review test architecture
- Ensure best practices
- Approve coverage strategy

---

## 🔐 Security Testing

### Key Areas
- Authentication (JWT tokens, password hashing)
- Authorization (resource ownership)
- Input validation (SQL injection, XSS)
- Data security (encryption, secure headers)

### Tools
- Bandit (Python security linter)
- npm audit (Node.js dependencies)
- OWASP ZAP (vulnerability scanning - manual)

---

## ♿ Accessibility Testing

### WCAG 2.1 Level AA Requirements
- Keyboard navigation works
- Screen reader compatible
- Color contrast 4.5:1 minimum
- ARIA labels present
- Focus indicators visible

### Tools
- axe DevTools
- WAVE browser extension
- Lighthouse (Chrome DevTools)
- Manual keyboard testing

---

## 📈 Performance Testing

### Key Metrics
- API response times < 200ms (95th percentile)
- Page load time < 2s
- Time to interactive < 3s
- First contentful paint < 1s

### Tools
- Locust (load testing)
- Lighthouse (frontend performance)
- Chrome DevTools Performance tab

---

## 🚦 Release Checklist

### Before Release
- [ ] All automated tests passing
- [ ] Manual smoke testing completed
- [ ] Performance benchmarks met
- [ ] Security scan passed
- [ ] Accessibility audit completed
- [ ] Cross-browser testing done
- [ ] Zero critical bugs
- [ ] All P1 bugs resolved
- [ ] Known issues documented
- [ ] QA sign-off obtained

---

## 💡 Best Practices

### Test Writing
1. **Arrange-Act-Assert** pattern
2. **Clear test names** - describe what is being tested
3. **One assertion per test** (when possible)
4. **Use fixtures** for test data
5. **Mock external dependencies**
6. **Clean up after tests**

### Test Maintenance
1. **Keep tests up to date** with code changes
2. **Remove obsolete tests**
3. **Fix flaky tests** immediately
4. **Review test coverage** regularly
5. **Refactor tests** when needed

### Code Review
1. **Review tests** in every PR
2. **Verify test coverage** doesn't decrease
3. **Check for missing edge cases**
4. **Ensure tests are readable**

---

## 🆘 Getting Help

### Resources
- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing Library docs](https://testing-library.com/)
- [Playwright documentation](https://playwright.dev/)
- [Vitest documentation](https://vitest.dev/)

### Questions?
- Check existing test examples in the codebase
- Review test implementation examples document
- Ask in team chat
- Create a GitHub discussion

---

## 🔄 Continuous Improvement

### Regular Activities
- **Weekly**: Review test metrics
- **Sprint**: Update test tracking checklist
- **Monthly**: Review and update test strategy
- **Quarterly**: Comprehensive test suite audit

### Improvement Areas
- Increase test automation coverage
- Reduce test execution time
- Improve test reliability (reduce flakiness)
- Enhance test documentation
- Optimize CI/CD pipeline

---

## 📝 Quick Commands Cheat Sheet

```bash
# Backend Testing
cd backend
pytest                                    # Run all tests
pytest --cov=app --cov-report=html       # Coverage report
pytest -m unit                           # Unit tests only
pytest -v                                # Verbose output

# Backend Linting
black app/                               # Format code
ruff check app/                          # Lint code
mypy app/                                # Type check

# Frontend Testing (when implemented)
cd frontend
npm run test                             # Run tests
npm run test:coverage                    # With coverage
npm run test:watch                       # Watch mode
npm run test:e2e                         # E2E tests

# Frontend Linting
npm run lint                             # Lint code
npm run type-check                       # TypeScript check

# Build
cd frontend
npm run build                            # Build frontend

# Docker
docker-compose up -d                     # Start all services
docker-compose exec backend pytest       # Run backend tests in container
```

---

**Last Updated**: 2025-11-15  
**Document Owner**: QA Team  
**Version**: 1.0.0
