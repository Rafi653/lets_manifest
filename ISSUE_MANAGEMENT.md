# Issue Management Process

## Overview

This document outlines the complete process for assigning, tracking, and closing issues within the Copilot Agent System. Following these guidelines ensures consistent, efficient issue management across all agent roles.

## Table of Contents

1. [Issue Lifecycle](#issue-lifecycle)
2. [Assigning Issues](#assigning-issues)
3. [Tracking Progress](#tracking-progress)
4. [Closing Issues](#closing-issues)
5. [Sub-Issue Management](#sub-issue-management)
6. [Best Practices](#best-practices)

## Issue Lifecycle

Every issue goes through the following stages:

```
Created → Triaged → Assigned → In Progress → In Review → Closed
```

### Stage Details

#### 1. Created
- Issue is created using appropriate agent template
- Automatically labeled with `needs-triage`
- Awaiting review by Tech Lead or relevant agent lead

#### 2. Triaged
- Issue has been reviewed and validated
- Priority has been set
- Dependencies have been identified
- `needs-triage` label removed
- Issue is ready for assignment

#### 3. Assigned
- Team member is assigned to the issue
- Issue moves to their active work queue
- Target completion date may be set

#### 4. In Progress
- Work has started
- Regular updates posted to issue
- Blockers identified and escalated
- Status label updated to `in-progress`

#### 5. In Review
- Pull Request has been submitted
- PR is linked to the issue
- Code review is in progress
- Testing/validation underway
- Status label updated to `in-review`

#### 6. Closed
- Work is complete and merged
- Acceptance criteria met
- Documentation updated
- Issue closed with summary

## Assigning Issues

### Direct Assignment

**When to use:**
- Urgent or time-sensitive work
- Specialized knowledge required
- Specific team member requested
- Critical path items

**Process:**
1. Tech Lead or PM identifies the right person
2. Assigns directly via GitHub
3. Notifies assignee with @mention in comment
4. Sets deadline if applicable
5. Adds `assigned` label

### Self-Assignment (Agent Pool)

**When to use:**
- Normal priority work
- Any qualified team member can handle it
- Team has capacity flexibility
- Encouraging team ownership

**Process:**
1. Issue remains unassigned after triage
2. Team members review available issues
3. Team member self-assigns based on:
   - Their expertise and agent role
   - Current workload
   - Interest in the task
4. Comments on issue to claim it
5. Updates status to `in-progress`

### Assignment Guidelines

**Capacity Considerations:**
- Each team member should have 2-4 active issues max
- Balance between different types of work
- Consider issue complexity and estimated time
- Leave room for urgent issues

**Fair Distribution:**
- Rotate interesting/challenging work
- Ensure junior members get learning opportunities
- Balance between agents during sprints
- Track assignment metrics to ensure fairness

## Tracking Progress

### Regular Updates

**For Assignees:**
- Comment on progress at least every 2 days
- Update when blocked or stuck
- Note any scope changes
- Link related PRs immediately

**Example Progress Comment:**
```markdown
### Progress Update

**Status:** 60% complete

**Completed:**
- [x] Database schema designed
- [x] API endpoint created
- [x] Unit tests written

**In Progress:**
- [ ] Integration testing

**Blockers:**
- Waiting on frontend mock-up (#123)

**ETA:** 2 days
```

### Status Labels

Update labels as work progresses:

- `needs-triage` → Initial state
- `ready` → Triaged and ready for work
- `in-progress` → Active work
- `blocked` → Cannot proceed (add blocker reason in comment)
- `in-review` → PR submitted
- `changes-requested` → PR needs updates

### Using GitHub Project Boards

If your repository uses project boards:

1. **Backlog** - Triaged but not started
2. **To Do** - Assigned and ready to start
3. **In Progress** - Active work
4. **In Review** - PR submitted
5. **Done** - Merged and closed

Move issues across columns as they progress.

### Handling Blockers

When blocked:

1. Add `blocked` label immediately
2. Comment with:
   - What is blocking
   - Who/what you're waiting for
   - Alternative approaches considered
3. Tag relevant team members
4. Escalate to Tech Lead if unresolved after 1 day
5. Update when blocker is resolved

**Example Blocker Comment:**
```markdown
🚧 **BLOCKED**

**Issue:** Cannot implement authentication flow until auth service is deployed

**Dependency:** #145 (BE auth service deployment)

**Blocking since:** 2024-01-15

**Workaround considered:** Could mock the service but would need to refactor later

@tech-lead @backend-team - Can we prioritize #145 or suggest alternative?
```

## Closing Issues

### Before Closing - Checklist

Ensure all items are complete:

- [ ] All acceptance criteria met
- [ ] Code merged to main/develop branch
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No open blockers or questions
- [ ] Related issues updated/closed
- [ ] Changes deployed (if applicable)

### Closing Comment Template

```markdown
## Closing Summary

**Resolution:** Completed as specified

**Changes Made:**
- Added user authentication endpoint
- Implemented JWT token generation
- Added unit and integration tests
- Updated API documentation

**Pull Request:** #234

**Testing:**
- ✅ Unit tests: 15/15 passing
- ✅ Integration tests: 8/8 passing
- ✅ Manual testing completed

**Documentation:**
- Updated API docs at `/docs/api/auth.md`
- Added example requests to README

**Related Issues:**
- Closes #120 (duplicate)
- Related to #125 (frontend integration)

**Notes:**
No known issues. Ready for production deployment.
```

### Close Without Implementation

Sometimes issues are closed without implementation:

**Reasons:**
- Duplicate of another issue
- Out of scope
- No longer relevant
- Cannot reproduce (for bugs)
- Won't fix

**Process:**
1. Add appropriate label: `duplicate`, `wontfix`, `invalid`
2. Comment explaining why
3. Link to related issues if duplicate
4. Close the issue

**Example:**
```markdown
Closing as duplicate of #156 which already addresses this feature.

Please track progress on #156 instead.
```

## Sub-Issue Management

### Creating Sub-Issues

For large features that span multiple agents:

1. **Parent Issue (Tech Lead)**
   - Create main feature issue using Tech Lead template
   - Label with `epic` or `parent`
   - Outline overall goal and architecture
   - List all required sub-issues

2. **Sub-Issues (Various Agents)**
   - Create individual issues for each agent
   - Use appropriate agent template
   - Link to parent issue in description
   - Note dependencies on other sub-issues
   - Label with `sub-issue`

**Example Parent Issue Structure:**
```markdown
# Feature: User Dashboard

## Overview
Implement a comprehensive user dashboard showing activity, stats, and recommendations.

## Architecture
[Diagram or description]

## Sub-Issues
- [ ] #201 [PM] Define dashboard metrics and layout
- [ ] #202 [BE] Create dashboard data API
- [ ] #203 [FE] Implement dashboard UI
- [ ] #204 [QA] Dashboard test plan and execution

## Dependencies
- BE (#202) must complete before FE (#203) can finish
- PM (#201) should inform all technical work

## Timeline
Sprint 12 (March 1-15)
```

### Tracking Sub-Issues

**In Parent Issue:**
- Keep checklist updated as sub-issues close
- Post weekly status updates
- Coordinate dependencies
- Escalate blockers

**In Sub-Issues:**
- Always reference parent issue
- Note dependencies on sibling issues
- Tag parent issue when blocked
- Comment when complete

### Closing Sub-Issues

1. Close each sub-issue individually when complete
2. Update parent issue checklist
3. Add comment to parent issue
4. When all sub-issues closed, close parent

## Best Practices

### Communication

✅ **Do:**
- Update issues regularly
- Be specific about blockers
- Tag relevant people
- Link related issues and PRs
- Use clear, concise language

❌ **Don't:**
- Leave issues without updates for days
- Use vague status updates
- Skip closing comments
- Forget to link PRs

### Time Management

✅ **Do:**
- Break down large tasks
- Estimate realistically
- Request help when stuck
- Update ETAs when they change

❌ **Don't:**
- Take on too many issues
- Underestimate complexity
- Hide when behind schedule
- Rush to close without quality

### Quality

✅ **Do:**
- Meet all acceptance criteria
- Write/update tests
- Update documentation
- Get proper code review
- Verify changes work as expected

❌ **Don't:**
- Close issues with failing tests
- Skip documentation
- Merge without review
- Leave TODOs in production code

### Collaboration

✅ **Do:**
- Help others when asked
- Share knowledge in comments
- Offer constructive feedback
- Celebrate completions

❌ **Don't:**
- Work in isolation
- Ignore requests for help
- Bypass review processes
- Blame others for delays

## Metrics and Reporting

### Individual Metrics
- Issue resolution time
- Number of active/completed issues
- Blocker frequency and resolution
- Code review turnaround

### Team Metrics
- Sprint completion rate
- Cross-agent coordination efficiency
- Average time in each stage
- Reopened issue rate

### Using Metrics
- Identify bottlenecks
- Improve estimation
- Balance workload
- Recognize achievements

## Troubleshooting

### Issue is blocked for too long
1. Comment with escalation
2. Tag Tech Lead
3. Discuss in team sync
4. Consider alternative approaches
5. May need to re-prioritize

### Scope creep during implementation
1. Document new requirements in comment
2. Discuss with PM and Tech Lead
3. Create separate issue for added scope
4. Keep original issue focused
5. Update acceptance criteria if agreed

### Can't meet deadline
1. Comment immediately when realized
2. Explain reasons
3. Provide new ETA
4. Request help if needed
5. Update stakeholders

### Unclear requirements
1. Don't proceed with assumptions
2. Comment with specific questions
3. Tag issue creator and PM
4. Mark as `blocked` until clarified
5. Update once clear

## Templates

### Progress Update Template
```markdown
### Progress Update - [Date]

**Status:** [X]% complete

**Completed:**
- [x] Task 1
- [x] Task 2

**In Progress:**
- [ ] Task 3

**Blockers:** None / [Description]

**ETA:** [Date or "on track"]
```

### Blocker Template
```markdown
🚧 **BLOCKED**

**Issue:** [What is blocking]
**Dependency:** [What you're waiting for]
**Since:** [Date]
**Impact:** [How it affects the work]

@relevant-team
```

### Closing Template
```markdown
## Closing Summary

**Resolution:** [Completed/Duplicate/Won't Fix/etc.]

**Changes Made:**
- [List key changes]

**PR:** #[number]

**Testing:** [Test results]

**Documentation:** [Updates made]

**Related Issues:** [Links]

**Notes:** [Any additional context]
```

## Conclusion

Effective issue management is critical to the success of the Copilot Agent System. By following these processes:

- Issues are resolved efficiently
- Work is transparent and trackable
- Team members stay aligned
- Quality standards are maintained
- Coordination overhead is minimized

For more information, see:
- [AGENTS.md](./AGENTS.md) - Agent roles and responsibilities
- [ROADMAP.md](./ROADMAP.md) - Task distribution and planning

---

**Questions or suggestions?** Open an issue with the `type:documentation` label or discuss in team meetings.
