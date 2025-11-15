# Contributing to Let's Manifest

Thank you for considering contributing to Let's Manifest! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful, inclusive, and considerate in all interactions. We aim to maintain a welcoming community for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Rafi653/lets_manifest/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Features

1. Check if the feature has been suggested in [Issues](https://github.com/Rafi653/lets_manifest/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Write clear, self-documenting code
   - Add comments for complex logic
   - Update documentation as needed

4. **Test your changes**
   - Write unit tests for new functionality
   - Ensure all tests pass
   - Check code coverage
   - Test manually in the UI

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add user profile feature"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Test additions or changes
   - `chore:` - Build process or auxiliary tool changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear title and description
   - Reference related issues
   - Include screenshots for UI changes
   - Wait for review and address feedback

## Development Setup

See [Setup Guide](setup.md) for detailed instructions.

Quick start:
```bash
git clone https://github.com/Rafi653/lets_manifest.git
cd lets_manifest
docker-compose up -d
```

## Code Style Guidelines

### Frontend (TypeScript/React)

- Use TypeScript for all new files
- Use functional components with hooks
- Follow React best practices
- Use meaningful component and variable names
- Keep components small and focused (< 200 lines)
- Co-locate component files with styles and tests
- Use CSS Modules or styled-components
- Avoid inline styles except for dynamic values
- Use ESLint and Prettier
- Add JSDoc comments for complex functions

**Example:**
```typescript
// Good
interface UserProfileProps {
  userId: string;
  onUpdate: (user: User) => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId, onUpdate }) => {
  const [user, setUser] = useState<User | null>(null);
  
  // Implementation...
};

// Bad
export function UserProfile(props) {
  const user = props.user;
  // Implementation...
}
```

### Backend (Python/FastAPI)

- Follow PEP 8 style guide
- Use type hints for all functions
- Keep functions small and focused
- Use async/await for database operations
- Keep business logic in services, not endpoints
- Use repository pattern for data access
- Use Black for formatting
- Use Ruff for linting
- Add docstrings for classes and functions

**Example:**
```python
# Good
async def get_user_by_email(
    email: str,
    db: AsyncSession
) -> User | None:
    """
    Retrieve a user by their email address.
    
    Args:
        email: The user's email address
        db: Database session
        
    Returns:
        User object if found, None otherwise
    """
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

# Bad
def getUserByEmail(email, db):
    result = db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()
```

## Testing Guidelines

### Frontend Tests

- Write unit tests for components
- Write integration tests for feature flows
- Use React Testing Library
- Test user interactions, not implementation
- Aim for 80%+ coverage

**Example:**
```typescript
describe('UserProfile', () => {
  it('should display user information', () => {
    const user = { id: '1', name: 'John Doe' };
    render(<UserProfile user={user} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});
```

### Backend Tests

- Write unit tests for services and repositories
- Write integration tests for API endpoints
- Use pytest fixtures
- Mock external dependencies
- Test edge cases and error conditions
- Aim for 80%+ coverage

**Example:**
```python
@pytest.mark.asyncio
async def test_create_user_success(db_session: AsyncSession):
    """Test successful user creation."""
    user_data = UserCreate(
        email="test@example.com",
        password="SecurePass123!",
        full_name="Test User"
    )
    
    user = await user_service.create_user(user_data, db_session)
    
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
```

## Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes
- `chore/` - Maintenance tasks

Examples:
- `feature/user-authentication`
- `fix/journal-entry-validation`
- `docs/api-endpoints`

## Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting, missing semicolons, etc.
- `refactor` - Code restructuring
- `test` - Adding tests
- `chore` - Maintenance tasks

**Examples:**
```
feat(auth): add JWT token refresh endpoint

fix(journal): resolve date formatting issue in entries

docs(api): update authentication documentation

test(user): add tests for user profile update
```

## Review Process

1. **Automated Checks**
   - All tests must pass
   - Code coverage must meet threshold
   - Linting must pass
   - Type checking must pass

2. **Manual Review**
   - Code quality and style
   - Architecture alignment
   - Security considerations
   - Performance implications
   - Documentation completeness

3. **Feedback**
   - Address reviewer comments
   - Make requested changes
   - Re-request review when ready

4. **Merge**
   - Squash and merge for clean history
   - Delete branch after merge

## Documentation

- Update relevant documentation with your changes
- Add JSDoc/docstrings for new functions
- Update API documentation for endpoint changes
- Add README updates for new features
- Include inline comments for complex logic

## Questions?

- Ask in [GitHub Discussions](https://github.com/Rafi653/lets_manifest/discussions)
- Comment on the related issue
- Reach out to maintainers

Thank you for contributing! 🎉
