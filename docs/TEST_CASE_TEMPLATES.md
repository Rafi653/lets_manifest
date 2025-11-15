# Test Case Templates

This document provides standardized templates for creating test cases across different test types.

---

## Test Case Template (Standard)

```markdown
## Test Case ID: [TC-XXX]

### Metadata
- **Module**: [Goals/Habits/Auth/etc.]
- **Feature**: [Specific feature being tested]
- **Type**: [Unit/Integration/E2E/Functional/Non-Functional]
- **Priority**: [Critical/High/Medium/Low]
- **Automated**: [Yes/No/Planned]
- **Author**: [Name]
- **Created**: [Date]
- **Last Updated**: [Date]

### Description
[Brief description of what this test case validates]

### Pre-conditions
- [Condition 1]
- [Condition 2]
- [...]

### Test Data
- [Any specific data needed for the test]

### Test Steps
1. [Step 1]
2. [Step 2]
3. [...]

### Expected Results
- [Expected result 1]
- [Expected result 2]
- [...]

### Actual Results
[To be filled during test execution]

### Post-conditions
- [What state should the system be in after test]

### Dependencies
- [Any dependencies on other tests or features]

### Notes
[Any additional information]

### Test Execution History
| Date | Tester | Build | Result | Notes |
|------|--------|-------|--------|-------|
|      |        |       |        |       |
```

---

## Backend API Test Case Template

```markdown
## API Test Case: [TC-API-XXX]

### Endpoint Details
- **Method**: [GET/POST/PUT/DELETE/PATCH]
- **URL**: [/api/v1/...]
- **Module**: [Module name]
- **Priority**: [Critical/High/Medium/Low]

### Authentication
- **Required**: [Yes/No]
- **Token Type**: [Bearer/Basic/etc.]
- **User Role**: [Admin/User/Public]

### Request Details

#### Headers
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <token>"
}
```

#### Request Body
```json
{
  // Request payload
}
```

#### Query Parameters
- param1: value1
- param2: value2

### Expected Response

#### Success Response (Status: XXX)
```json
{
  "data": {},
  "message": "Success message",
  "errors": null,
  "meta": {}
}
```

#### Error Response (Status: XXX)
```json
{
  "data": null,
  "message": "Error message",
  "errors": [],
  "meta": {}
}
```

### Validation Checks
- [ ] Status code is correct
- [ ] Response structure matches schema
- [ ] Required fields are present
- [ ] Data types are correct
- [ ] Business logic is applied correctly
- [ ] Error handling works as expected
- [ ] Response time is acceptable (<XXXms)

### Edge Cases to Test
1. [Edge case 1]
2. [Edge case 2]

### Test Implementation
```python
async def test_endpoint_name():
    # Test code here
    pass
```
```

---

## Frontend Component Test Case Template

```markdown
## Component Test: [TC-UI-XXX]

### Component Details
- **Component Name**: [ComponentName]
- **File Path**: [src/components/...]
- **Priority**: [Critical/High/Medium/Low]
- **Dependencies**: [List parent components or services]

### Description
[What this component does and what we're testing]

### Props
```typescript
interface ComponentProps {
  prop1: string;
  prop2: number;
  onAction?: () => void;
}
```

### Test Scenarios

#### 1. Rendering
- [ ] Component renders without crashing
- [ ] All expected elements are present
- [ ] Default props are applied correctly
- [ ] Conditional rendering works

#### 2. User Interactions
- [ ] Clicking buttons triggers correct actions
- [ ] Form inputs accept and validate data
- [ ] Keyboard navigation works
- [ ] Hover states display correctly

#### 3. State Management
- [ ] Component state updates correctly
- [ ] Props changes trigger re-render
- [ ] Side effects execute as expected

#### 4. Integration
- [ ] API calls are made with correct data
- [ ] Loading states display
- [ ] Error states display
- [ ] Success states display

### Test Implementation
```typescript
describe('ComponentName', () => {
  test('renders correctly', () => {
    // Test code
  });

  test('handles user interaction', async () => {
    // Test code
  });
});
```

### Accessibility Checks
- [ ] Keyboard accessible
- [ ] Screen reader friendly
- [ ] ARIA labels present
- [ ] Color contrast meets WCAG 2.1 AA
- [ ] Focus indicators visible
```

---

## E2E Test Case Template

```markdown
## E2E Test: [TC-E2E-XXX]

### User Journey
**Title**: [Journey name]
**Priority**: [Critical/High/Medium/Low]
**Frequency**: [Every build/Pre-release/Weekly]

### Description
[Complete user workflow being tested]

### Actors
- **User Type**: [New user/Registered user/Admin]
- **Starting State**: [Not logged in/Logged in/etc.]

### Pre-conditions
- [System state before test]
- [Test data requirements]
- [Environment setup]

### Test Flow

#### Step 1: [Action]
- **User Action**: [What the user does]
- **Expected Result**: [What should happen]
- **Verification**: [How to verify]

#### Step 2: [Action]
- **User Action**: [What the user does]
- **Expected Result**: [What should happen]
- **Verification**: [How to verify]

[Continue for all steps...]

### Success Criteria
- [ ] User can complete the entire flow
- [ ] All data is saved correctly
- [ ] UI updates appropriately
- [ ] No errors occur
- [ ] Performance is acceptable

### Alternative Paths
1. **Path Name**: [e.g., "User cancels operation"]
   - [Steps for this path]

### Error Scenarios
1. **Scenario**: [e.g., "Network failure during save"]
   - **Expected**: [How system should handle]

### Test Data
```javascript
const testData = {
  user: {
    email: "test@example.com",
    password: "TestPass123!"
  },
  // Other data
}
```

### Test Implementation
```typescript
test('User can complete [journey]', async ({ page }) => {
  // Playwright test code
});
```

### Screenshots/Videos
- [Attach evidence of test execution]

### Performance Benchmarks
- Total journey time: < X seconds
- Page load times: < X seconds each
```

---

## Integration Test Case Template

```markdown
## Integration Test: [TC-INT-XXX]

### Integration Scope
- **Components**: [List of components/modules being tested together]
- **Type**: [Component Integration/API Integration/Database Integration]
- **Priority**: [Critical/High/Medium/Low]

### Description
[What integration is being tested]

### Architecture
```
[Component A] ←→ [Component B] ←→ [Component C]
```

### Dependencies
- [External service 1]
- [Database]
- [Message queue]
- [etc.]

### Test Scenarios

#### Scenario 1: [Happy Path]
**Setup**:
- [Initial state]

**Actions**:
1. [Action 1]
2. [Action 2]

**Verifications**:
- [ ] Component A receives correct data
- [ ] Component B processes data correctly
- [ ] Component C stores data correctly
- [ ] All components communicate successfully

#### Scenario 2: [Error Handling]
**Setup**:
- [Setup for error condition]

**Actions**:
- [Trigger error]

**Verifications**:
- [ ] Error is caught and handled
- [ ] System remains stable
- [ ] User receives appropriate feedback

### Data Flow
```
Input → [Processing] → Output
```

### Test Implementation
```python
async def test_integration_scenario():
    # Test code
    pass
```

### Cleanup
- [Steps to clean up test data]
```

---

## Performance Test Case Template

```markdown
## Performance Test: [TC-PERF-XXX]

### Test Objective
[What performance aspect is being tested]

### Test Type
- [ ] Load Test
- [ ] Stress Test
- [ ] Spike Test
- [ ] Endurance Test
- [ ] Scalability Test

### Test Parameters
- **User Load**: [Number of concurrent users]
- **Duration**: [Test duration]
- **Ramp-up Time**: [Time to reach peak load]
- **Environment**: [Test environment details]

### Performance Metrics
- **Response Time**: Target < XXX ms (95th percentile)
- **Throughput**: Target > XXX requests/second
- **Error Rate**: Target < X%
- **CPU Usage**: Target < XX%
- **Memory Usage**: Target < XX%
- **Database Connections**: Target < XXX

### Test Scenario
1. [User action 1] - XX% of users
2. [User action 2] - XX% of users
3. [User action 3] - XX% of users

### Test Script
```python
# Locust example
from locust import HttpUser, task, between

class PerformanceTest(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def list_goals(self):
        self.client.get("/api/v1/goals")
    
    @task(1)
    def create_goal(self):
        self.client.post("/api/v1/goals", json={...})
```

### Baseline Metrics
| Metric | Baseline | Current | Target | Status |
|--------|----------|---------|--------|--------|
| Response Time | 150ms | 145ms | <200ms | ✅ |
| Throughput | 500 rps | 520 rps | >450 rps | ✅ |

### Results
[To be filled after test execution]

### Bottlenecks Identified
- [Issue 1]
- [Issue 2]

### Recommendations
- [Recommendation 1]
- [Recommendation 2]
```

---

## Security Test Case Template

```markdown
## Security Test: [TC-SEC-XXX]

### Security Area
- [ ] Authentication
- [ ] Authorization
- [ ] Input Validation
- [ ] SQL Injection
- [ ] XSS (Cross-Site Scripting)
- [ ] CSRF (Cross-Site Request Forgery)
- [ ] Session Management
- [ ] Data Encryption
- [ ] API Security

### Vulnerability Type
[OWASP Top 10 category if applicable]

### Description
[What security aspect is being tested]

### Attack Vectors
1. [Attack vector 1]
2. [Attack vector 2]

### Test Steps
1. [Step to attempt vulnerability]
2. [Step to verify protection]

### Expected Security Behavior
- [How system should protect against this attack]
- [What security controls should activate]

### Test Cases

#### Test 1: [Specific security test]
**Attack**: [What attack is attempted]
**Expected**: [How system should respond]
**Actual**: [Observed behavior]
**Status**: [Pass/Fail]

### Tools Used
- [Burp Suite]
- [OWASP ZAP]
- [SQL Map]
- [etc.]

### Severity Assessment
- **CVSS Score**: [If applicable]
- **Risk Level**: [Critical/High/Medium/Low]
- **Exploitability**: [Easy/Medium/Hard]
- **Impact**: [Severe/Moderate/Low]

### Remediation
[If vulnerability found, describe fix]

### Verification
[How to verify the fix works]
```

---

## Accessibility Test Case Template

```markdown
## Accessibility Test: [TC-A11Y-XXX]

### WCAG Compliance Level
- [ ] Level A
- [ ] Level AA
- [ ] Level AAA

### Component/Page
[Component or page being tested]

### Accessibility Criteria

#### 1. Perceivable
- [ ] Text alternatives for non-text content
- [ ] Captions for audio/video
- [ ] Content adaptable to different presentations
- [ ] Sufficient color contrast (4.5:1 for normal text)

#### 2. Operable
- [ ] All functionality available via keyboard
- [ ] No keyboard traps
- [ ] Adjustable time limits
- [ ] Clear focus indicators
- [ ] Skip navigation links

#### 3. Understandable
- [ ] Clear language
- [ ] Predictable navigation
- [ ] Input assistance and error identification
- [ ] Labels and instructions provided

#### 4. Robust
- [ ] Valid HTML
- [ ] Compatible with assistive technologies
- [ ] ARIA attributes used correctly

### Testing Tools
- [ ] axe DevTools
- [ ] WAVE
- [ ] Screen reader (NVDA/JAWS/VoiceOver)
- [ ] Keyboard navigation
- [ ] Color contrast analyzer

### Test Scenarios

#### Keyboard Navigation
1. Tab through all interactive elements
2. Verify tab order is logical
3. Verify all actions can be performed with keyboard
4. No keyboard traps exist

#### Screen Reader
1. All content is announced
2. Headings are properly structured
3. Links have descriptive text
4. Form labels are associated correctly
5. ARIA labels are read correctly

### Issues Found
| Issue | WCAG Criterion | Severity | Status |
|-------|----------------|----------|--------|
|       |                |          |        |

### Recommendations
- [Recommendation 1]
- [Recommendation 2]
```

---

## Regression Test Case Template

```markdown
## Regression Test: [TC-REG-XXX]

### Original Bug/Feature
- **Bug ID**: [If testing a bug fix]
- **Feature**: [If testing a feature]
- **Release**: [Version where it was introduced/fixed]

### Risk Areas
[Areas of the application that might be affected]

### Test Scope
- [ ] Core functionality unchanged
- [ ] Related features work correctly
- [ ] No new bugs introduced
- [ ] Performance not degraded

### Original Test Cases to Re-run
- [TC-XXX]: [Test case name]
- [TC-YYY]: [Test case name]

### Additional Verification
1. [Specific check 1]
2. [Specific check 2]

### Test Results
| Test Case | Previous Result | Current Result | Status |
|-----------|----------------|----------------|--------|
| TC-XXX    | Pass           | Pass           | ✅     |
| TC-YYY    | Pass           | Pass           | ✅     |

### Regression Risks
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]
```

---

## Exploratory Test Charter Template

```markdown
## Exploratory Test Charter: [CHARTER-XXX]

### Mission
[What are we exploring and why?]

### Time Box
**Duration**: [30/60/90 minutes]
**Start Time**: [Time]
**End Time**: [Time]

### Scope
**In Scope**:
- [Area 1]
- [Area 2]

**Out of Scope**:
- [Area 1]
- [Area 2]

### Strategy/Approach
[How will you explore this area?]

### Test Ideas
1. [Idea 1]
2. [Idea 2]
3. [Idea 3]

### Areas Covered
- [Area 1] - [Time spent]
- [Area 2] - [Time spent]

### Findings

#### Bugs
| ID | Description | Severity | Steps to Reproduce |
|----|-------------|----------|-------------------|
|    |             |          |                   |

#### Questions/Concerns
1. [Question 1]
2. [Question 2]

#### Positive Observations
- [Good thing 1]
- [Good thing 2]

### Test Data Used
- [Data set 1]
- [User account]
- [etc.]

### Notes
[Any additional observations, patterns noticed, or ideas for future testing]

### Follow-up Actions
- [ ] Create bug reports for issues found
- [ ] Add test cases for scenarios discovered
- [ ] Further exploration needed in [area]
```

---

## Test Summary Report Template

```markdown
## Test Summary Report

### Report Details
- **Project**: Let's Manifest
- **Release**: [Version]
- **Test Cycle**: [Sprint/Release name]
- **Report Date**: [Date]
- **Test Lead**: [Name]

### Executive Summary
[Brief overview of testing activities and results]

### Test Metrics

#### Test Execution
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Test Cases | XXX | 100% |
| Executed | XXX | XX% |
| Passed | XXX | XX% |
| Failed | XXX | XX% |
| Blocked | XXX | XX% |
| Not Executed | XXX | XX% |

#### Defects
| Severity | Open | Fixed | Closed | Total |
|----------|------|-------|--------|-------|
| Critical | X | X | X | X |
| High | X | X | X | X |
| Medium | X | X | X | X |
| Low | X | X | X | X |

#### Code Coverage
- Backend: XX%
- Frontend: XX%

### Test Activities
1. [Activity 1] - [Status]
2. [Activity 2] - [Status]

### Areas Tested
- [Module 1] - [XX test cases] - [XX% pass rate]
- [Module 2] - [XX test cases] - [XX% pass rate]

### Defects Summary
#### Critical/High Issues
1. [BUG-XXX]: [Description] - [Status]
2. [BUG-YYY]: [Description] - [Status]

#### Known Issues
- [Issue 1] - [Workaround if any]
- [Issue 2] - [Workaround if any]

### Risks and Concerns
1. [Risk 1] - [Severity] - [Mitigation]
2. [Risk 2] - [Severity] - [Mitigation]

### Test Environment
- **Backend**: [Version/Environment details]
- **Frontend**: [Version/Environment details]
- **Database**: [Version]
- **Browsers**: [List]

### Schedule
- **Test Start Date**: [Date]
- **Test End Date**: [Date]
- **Actual Duration**: [X days]

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

### Release Readiness
**Status**: [Go / No-Go / Conditional]

**Justification**: [Explanation of recommendation]

### Sign-off
- **QA Lead**: ________________ Date: ______
- **Tech Lead**: ________________ Date: ______
- **Product Manager**: ________________ Date: ______
```

---

## Usage Guidelines

### When to Use Each Template

1. **Standard Test Case**: General functional testing
2. **API Test Case**: Testing backend endpoints
3. **Component Test Case**: Testing React components
4. **E2E Test Case**: Testing complete user journeys
5. **Integration Test Case**: Testing multiple components together
6. **Performance Test Case**: Load, stress, or performance testing
7. **Security Test Case**: Security vulnerability testing
8. **Accessibility Test Case**: WCAG compliance testing
9. **Regression Test Case**: Verifying no regressions after changes
10. **Exploratory Charter**: Time-boxed exploratory testing
11. **Test Summary**: Reporting test results to stakeholders

### Best Practices

1. **Be Specific**: Clear, unambiguous test steps
2. **Use Test Data**: Include realistic test data
3. **Document Everything**: Include screenshots, logs, etc.
4. **Update Regularly**: Keep test cases current
5. **Track History**: Maintain execution history
6. **Link Issues**: Reference related bugs/features
7. **Review Regularly**: Peer review test cases

### Test Case Maintenance

- Review test cases quarterly
- Update when features change
- Archive obsolete tests
- Maintain traceability to requirements
- Keep automation in sync with manual tests
