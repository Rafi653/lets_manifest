# Copilot Agent System

## Overview

The Copilot Agent System is a structured approach to managing development tasks through role-based issue delegation. This system ensures that work is properly scoped, assigned, and tracked across different functional areas of the project.

## Agent Roles

### 1. Product Manager (PM) Agent
**Label:** `agent:pm`

**Responsibilities:**
- Define product requirements and user stories
- Prioritize features and manage product backlog
- Gather and analyze user feedback
- Create product roadmaps
- Make product-related decisions
- Coordinate with stakeholders
- Validate that features meet business objectives

**When to Use:**
- Creating new feature specifications
- Prioritizing work across the product
- Defining user personas and journeys
- Making product tradeoff decisions
- Planning releases and milestones

### 2. Frontend Engineer (FE) Agent
**Label:** `agent:frontend`

**Responsibilities:**
- Implement user interfaces and UI components
- Ensure responsive and accessible design
- Manage client-side state and data flow
- Integrate with backend APIs
- Optimize frontend performance
- Implement client-side testing
- Maintain styling consistency

**When to Use:**
- Building or modifying UI components
- Implementing new pages or views
- Fixing visual or interaction bugs
- Optimizing frontend performance
- Adding client-side features
- Improving accessibility

### 3. Backend Engineer (BE) Agent
**Label:** `agent:backend`

**Responsibilities:**
- Design and implement APIs
- Manage database schema and migrations
- Implement business logic
- Handle authentication and authorization
- Integrate with external services
- Optimize server-side performance
- Write backend tests

**When to Use:**
- Creating or modifying API endpoints
- Implementing business logic
- Database design and migrations
- Third-party service integrations
- Server-side performance optimization
- Security implementations

### 4. Quality Assurance (QA) Agent
**Label:** `agent:qa`

**Responsibilities:**
- Create and maintain test plans
- Write and execute test cases
- Perform manual and automated testing
- Report and verify bugs
- Ensure quality standards are met
- Test across different environments
- Validate requirements are met

**When to Use:**
- Planning testing for new features
- Creating test cases
- Performing regression testing
- Verifying bug fixes
- Conducting UAT
- Performance or security testing

### 5. Tech Lead Agent
**Label:** `agent:tech-lead`

**Responsibilities:**
- Make architectural decisions
- Plan technical roadmap
- Coordinate cross-functional work
- Review code and ensure quality
- Address technical debt
- Mentor and guide the team
- Resolve technical conflicts
- Ensure scalability and maintainability

**When to Use:**
- Making architecture decisions
- Planning major technical initiatives
- Coordinating work across multiple agents
- Resolving technical blockers
- Technical debt prioritization
- Setting coding standards
- Performance and scalability planning

## Workflow Process

### 1. Issue Creation
When creating a new issue, determine which agent role is most appropriate and use the corresponding issue template:
- Navigate to Issues → New Issue
- Select the appropriate agent template
- Fill in all required fields
- Add relevant labels and assignees

### 2. Issue Triage
New issues receive the `needs-triage` label. The Tech Lead or appropriate team member should:
1. Review the issue details
2. Validate it's assigned to the correct agent
3. Add additional context if needed
4. Set priority level
5. Remove `needs-triage` label
6. Assign to appropriate team member or leave unassigned for the agent to pick up

### 3. Task Assignment
Tasks can be assigned in two ways:
- **Direct Assignment:** A team member is directly assigned to the issue
- **Agent Pool:** Issue is left unassigned for the relevant agent team to self-assign based on capacity

### 4. Work Execution
1. Assignee moves issue to "In Progress"
2. Assignee implements the required changes
3. Assignee creates a Pull Request and links it to the issue
4. Code review process is followed
5. Once approved and merged, issue is closed

### 5. Cross-Agent Coordination
For features requiring multiple agents:
1. Tech Lead creates a parent issue outlining the overall feature
2. Sub-issues are created for each agent with appropriate templates
3. Dependencies are noted in each sub-issue
4. Tech Lead monitors progress and coordinates across agents
5. Parent issue is closed when all sub-issues are complete

## Issue Labeling Convention

### Agent Labels (Primary)
- `agent:pm` - Product Manager tasks
- `agent:frontend` - Frontend Engineer tasks
- `agent:backend` - Backend Engineer tasks
- `agent:qa` - Quality Assurance tasks
- `agent:tech-lead` - Tech Lead tasks

### Status Labels
- `needs-triage` - Needs initial review
- `blocked` - Cannot proceed due to dependency
- `ready` - Ready to be worked on
- `in-progress` - Currently being worked on
- `in-review` - Pull request submitted

### Priority Labels
- `priority:p0` - Critical, drop everything
- `priority:p1` - High priority
- `priority:p2` - Medium priority
- `priority:p3` - Low priority

### Type Labels
- `type:feature` - New feature or enhancement
- `type:bug` - Something isn't working
- `type:documentation` - Documentation improvements
- `type:refactor` - Code refactoring
- `type:technical-debt` - Technical debt items

## Best Practices

### For Issue Creators
1. Use the appropriate agent template
2. Provide clear, detailed descriptions
3. Include acceptance criteria
4. Note dependencies
5. Set realistic priorities
6. Add relevant context and links

### For Assignees
1. Update issue status regularly
2. Ask questions if requirements are unclear
3. Document decisions made during implementation
4. Link PRs to issues
5. Update the issue before closing

### For Tech Leads
1. Review issues regularly for triage
2. Ensure dependencies are clear
3. Coordinate complex, multi-agent tasks
4. Monitor for blockers
5. Facilitate cross-team communication

### For Product Managers
1. Keep requirements clear and updated
2. Prioritize based on business value
3. Validate implementations meet requirements
4. Gather and incorporate feedback
5. Maintain product roadmap alignment

## Communication

- Use issue comments for asynchronous discussion
- Tag relevant team members with @mentions
- Reference related issues with #issue-number
- Update issue status when progress is made
- Close issues with clear resolution notes

## Metrics and Tracking

Track the following metrics to ensure system effectiveness:
- Issue resolution time by agent type
- Number of issues per priority level
- Blocked issues and resolution time
- Cross-agent coordination overhead
- Quality metrics (bugs per feature)

## Continuous Improvement

This agent system should evolve based on team feedback:
- Review process quarterly
- Gather feedback from all agent roles
- Adjust templates and workflows as needed
- Update documentation to reflect changes
- Share learnings across the team
