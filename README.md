# lets_manifest

## Overview

This project uses a structured Copilot Agent System for managing development tasks across different functional roles. This approach ensures clear ownership, proper task delegation, and efficient coordination across the team.

## Copilot Agent System

We use role-based agents to manage and coordinate work:

- **Product Manager (PM)** - Product requirements, roadmap, and feature prioritization
- **Frontend Engineer (FE)** - UI/UX implementation and client-side development
- **Backend Engineer (BE)** - API development, database, and server-side logic
- **Quality Assurance (QA)** - Testing, quality gates, and bug verification
- **Tech Lead** - Architecture, coordination, and technical leadership

## Getting Started

### Creating Issues

When creating a new issue, use the appropriate agent template:

1. Go to the **Issues** tab
2. Click **New Issue**
3. Select the template that matches your task:
   - `Product Manager Task` - for product and requirements work
   - `Frontend Engineer Task` - for UI and client-side development
   - `Backend Engineer Task` - for API and server-side development
   - `Quality Assurance Task` - for testing and QA work
   - `Tech Lead Task` - for architecture and coordination

### Documentation

- **[AGENTS.md](./AGENTS.md)** - Detailed information about each agent role, responsibilities, and workflows
- **[ROADMAP.md](./ROADMAP.md)** - Task distribution plan, phased approach, and coordination guidelines

## Workflow

1. **Create Issue** - Use the appropriate agent template
2. **Triage** - Tech Lead or PM reviews and sets priority
3. **Assign** - Issue is assigned or picked up by team member
4. **Implement** - Work is completed and PR is created
5. **Review** - Code review and testing
6. **Close** - Issue is closed upon merge

## Contributing

Please refer to [AGENTS.md](./AGENTS.md) for detailed guidelines on:
- When to use each agent type
- How to structure issues
- Cross-agent coordination
- Best practices

## Labels

Issues are labeled by agent type and priority:
- `agent:pm`, `agent:frontend`, `agent:backend`, `agent:qa`, `agent:tech-lead`
- `priority:p0`, `priority:p1`, `priority:p2`, `priority:p3`
- `type:feature`, `type:bug`, `type:documentation`, etc.

See [AGENTS.md](./AGENTS.md) for the complete labeling convention.