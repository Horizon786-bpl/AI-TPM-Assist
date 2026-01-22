# Jira Max Agent - Specification

## Overview

Jira Max is an advanced AI-powered Jira project management agent designed for Technical Program Managers (TPMs). It provides comprehensive capabilities for milestone tracking, sprint planning, issue analytics, dependency management, and worklog analysis.

## Quick Links

- [Requirements](./requirements.md) - Detailed user stories and acceptance criteria
- [Design](./design.md) - Architecture and technical design
- [Tasks](./tasks.md) - Implementation task breakdown

## Key Capabilities

### 1. Schedule-to-Jira Translation
- Import program schedules from Confluence
- Automatically create Jira versions, epics, and issues
- Set up dependencies based on schedule
- Sync changes back to Confluence

### 2. Milestone Management
- Track milestone progress (completed, in progress, to do)
- Analyze features vs bugs ratio
- Monitor worklog summaries (time logged, remaining, estimated)
- Identify risks (blocked issues, behind schedule, dependencies)

### 3. Sprint Planning
- Create sprints from milestones
- Balance workload across team members (AI-powered)
- Track sprint status and burndown
- Calculate velocity and predict completion

### 4. Issue Analytics
- Time-to-close analysis
- Velocity tracking
- Bottleneck identification
- Performance metrics dashboard

### 5. Dependency Management
- Create and visualize issue dependencies
- Identify critical paths
- Analyze dependency risks
- Detect circular dependencies

### 6. Worklog Analytics
- Track time logged per milestone/team member
- Analyze actual vs estimated effort
- Calculate team utilization
- Perform cost analysis

## Technology Stack

### MCP Integration
- **Atlassian MCP** (Primary): Sprints, links, worklogs, versions, batch operations
- **RBKS MCP** (Fallback): Basic Jira operations, Confluence access

### AI Integration
- **Claude 3.5 Sonnet**: Intent classification, schedule parsing, workload balancing, risk analysis, insight generation

### Infrastructure
- **LangGraph**: Workflow orchestration
- **Python 3.11+**: Implementation language
- **Redis** (Optional): Caching layer

## Architecture

```
Slack → LangGraph → Jira Max Agent → Sub-Agents → MCPs
                                    ↓
                              Claude AI Analysis
```

### Sub-Agents
1. **Milestone Manager** - Milestone tracking and reporting
2. **Sprint Planner** - Sprint creation and management
3. **Issue Analyzer** - Metrics and analytics
4. **Dependency Tracker** - Dependency management
5. **Worklog Analyzer** - Time tracking and cost analysis
6. **Schedule Importer** - Confluence schedule import

## Implementation Phases

### Phase 2A: Basic Analytics (Week 1-2)
- Issue search and filtering
- Basic metrics (open, closed, time-to-close)
- Features vs bugs analysis
- Simple reports

### Phase 2B: Milestone Management (Week 3-4)
- Milestone status reports
- Milestone comparison
- Worklog summaries
- Risk identification

### Phase 2C: Sprint Planning (Week 5-6)
- Sprint creation
- Workload distribution
- Sprint status tracking
- Velocity calculation

### Phase 2D: Advanced Features (Week 7-8)
- Schedule import
- Dependency management
- Cost analysis
- Advanced analytics

### Phase 2E: Slack Integration (Week 9)
- Slack command handler
- Interactive UI
- Message formatting
- End-to-end testing

### Phase 2F: Documentation & Deployment (Week 10)
- User documentation
- Technical documentation
- Deployment
- Monitoring setup

## Example Commands

```
# Milestone status
/jira-max status DVT

# Create sprint
/jira-max sprint create DVT --capacity 80

# Issue analytics
/jira-max analytics RCIT --days 30

# Import schedule
/jira-max import schedule https://confluence.../page/123456

# Dependency analysis
/jira-max dependencies RCIT-1234

# Worklog report
/jira-max worklog DVT --by-team-member
```

## Success Metrics

1. **Adoption:** 80% of TPMs use Jira Max weekly
2. **Time Savings:** 5+ hours saved per TPM per week
3. **Accuracy:** 95%+ accuracy in schedule imports
4. **Performance:** <10s response time for 90% of queries
5. **Satisfaction:** 4.5+ star rating from users

## Prerequisites

### Required
- Atlassian MCP server installed and configured
- RBKS MCP server (already available)
- Jira API access with appropriate permissions
- Confluence API access
- Bedrock Claude access

### Optional
- Redis for caching
- Monitoring infrastructure

## Getting Started

1. Review the [Requirements](./requirements.md) document
2. Understand the [Design](./design.md) architecture
3. Follow the [Tasks](./tasks.md) implementation plan
4. Start with Phase 2A (Basic Analytics)

## Related Agents

- **Agent #1 (Status Summarizer)** - Program status reporting
- **Agent #2 (Risk Analyzer)** - Risk identification and tracking
- **Agent #3 (Team Roster)** - Team member information

## Support

For questions or issues:
1. Check the documentation
2. Review the troubleshooting guide
3. Contact the TPM Assistant team

## License

Internal use only - Ring/Blink/Key/Sidewalk TPM teams
