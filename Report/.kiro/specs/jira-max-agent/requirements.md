# Jira Max Agent - Requirements Specification

## Overview

**Agent Name:** Jira Max (Agent #4)  
**Purpose:** Advanced Jira project management, workload tracking, and analytics  
**Priority:** Phase 2  
**Dependencies:** Atlassian MCP + RBKS MCP  

## Problem Statement

TPMs need to:
1. Translate program schedules from Confluence into Jira execution plans
2. Track milestone progress with features vs bugs breakdown
3. Manage sprint planning and team workload distribution
4. Analyze issue metrics (time-to-close, velocity, bottlenecks)
5. Visualize and manage dependencies between issues
6. Track actual time spent vs estimates using worklogs

Currently, this requires manual work across multiple Jira screens and spreadsheets.

## User Stories

### Epic 1: Schedule-to-Jira Translation

**US-1.1: Import Program Schedule**
```
As a TPM
I want to import a program schedule from Confluence to Jira
So that I can automatically create issues for all deliverables

Acceptance Criteria:
- Parse Confluence page with program schedule
- Extract milestones (DVT, PVT, MP, etc.)
- Create Jira versions for each milestone
- Create epics for major deliverables
- Create issues for each task with:
  - Summary from schedule
  - Description
  - Assignee (if specified)
  - Due date
  - Story points/estimate
  - Link to milestone version
- Set up dependencies based on schedule
- Generate summary report of created issues
```

**US-1.2: Update Schedule from Jira**
```
As a TPM
I want to sync Jira changes back to Confluence schedule
So that the schedule stays up-to-date

Acceptance Criteria:
- Detect changes in Jira (status, dates, assignees)
- Update corresponding Confluence schedule table
- Add comment noting sync timestamp
- Handle conflicts gracefully
```

### Epic 2: Milestone Management

**US-2.1: Milestone Status Report**
```
As a TPM
I want to see the status of a specific milestone
So that I can track progress and identify risks

Acceptance Criteria:
- Show milestone target date and days remaining
- Display issue breakdown:
  - Completed count and %
  - In Progress count and %
  - To Do count and %
- Show features vs bugs ratio
- Display worklog summary:
  - Time logged
  - Time remaining
  - Estimated total
- Identify risks:
  - Blocked issues
  - Behind schedule issues
  - Dependency issues
- Format as readable Slack message
```

**US-2.2: Milestone Comparison**
```
As a TPM
I want to compare progress across all milestones
So that I can see which milestones are at risk

Acceptance Criteria:
- List all milestones for program
- Show completion % for each
- Show on-time vs behind schedule
- Highlight milestones at risk
- Sort by target date
```

**US-2.3: Features vs Bugs Analysis**
```
As a TPM
I want to see features vs bugs breakdown per milestone
So that I can assess quality and scope

Acceptance Criteria:
- Count features and bugs separately
- Calculate ratio (% bugs)
- Show trend over time
- Alert if bug ratio exceeds threshold (e.g., >30%)
- Recommend actions (e.g., "Consider bug bash")
```

### Epic 3: Sprint Planning & Workload

**US-3.1: Create Sprint from Milestone**
```
As a TPM
I want to create a sprint for a milestone
So that I can plan team work for the next 2 weeks

Acceptance Criteria:
- Get unassigned issues for milestone
- Calculate team capacity (team size × hours per sprint)
- Select issues that fit capacity
- Balance workload across team members
- Create sprint with:
  - Name (e.g., "Sprint 23 - DVT")
  - Start and end dates
  - Goal description
- Assign issues to sprint
- Generate sprint summary:
  - Issue count
  - Features vs bugs
  - Workload per person
  - Capacity utilization %
```

**US-3.2: Sprint Status**
```
As a TPM
I want to see current sprint status
So that I can track daily progress

Acceptance Criteria:
- Show sprint name and dates
- Display burndown:
  - Story points completed
  - Story points remaining
  - Ideal burndown line
  - Actual burndown line
- Show issue status breakdown
- List blocked issues
- Calculate velocity
- Predict completion date
```

**US-3.3: Team Workload Distribution**
```
As a TPM
I want to see workload distribution across team
So that I can balance work and avoid burnout

Acceptance Criteria:
- List all team members
- Show assigned issues per person
- Calculate total hours per person
- Show capacity utilization %
- Identify over-allocated members (>100%)
- Identify under-allocated members (<70%)
- Suggest rebalancing
```

### Epic 4: Issue Analytics

**US-4.1: Issue Metrics Dashboard**
```
As a TPM
I want to see overall issue metrics for my program
So that I can track team performance

Acceptance Criteria:
- Show issue status breakdown (open, in progress, closed)
- Calculate time-to-close metrics:
  - Average
  - Median
  - Min/max
- Show features vs bugs ratio
- Display velocity trend (last 6 sprints)
- Identify bottlenecks (stages with longest duration)
- Format as dashboard with charts
```

**US-4.2: Time-to-Close Analysis**
```
As a TPM
I want to analyze how long issues take to close
So that I can identify process improvements

Acceptance Criteria:
- Calculate time-to-close for each issue
- Group by issue type (bug, feature, task)
- Show distribution (histogram)
- Identify outliers (>2 std dev)
- Show time spent in each status
- Recommend process improvements
```

**US-4.3: Velocity Tracking**
```
As a TPM
I want to track team velocity over time
So that I can predict future capacity

Acceptance Criteria:
- Calculate story points completed per sprint
- Show velocity trend (last 6 sprints)
- Calculate average velocity
- Show velocity variance
- Predict next sprint capacity
- Alert on significant velocity drops
```

### Epic 5: Dependency Management

**US-5.1: Create Dependencies**
```
As a TPM
I want to create dependencies between issues
So that I can track execution order

Acceptance Criteria:
- Support link types:
  - Blocks / Is blocked by
  - Depends on / Is depended on by
  - Relates to
- Create links between issues
- Validate no circular dependencies
- Update issue status if blocked
- Notify assignees of new dependencies
```

**US-5.2: Dependency Visualization**
```
As a TPM
I want to see all dependencies for an issue
So that I can understand the impact

Acceptance Criteria:
- Show upstream dependencies (blocks)
- Show downstream dependencies (depends on)
- Display dependency chain
- Identify critical path
- Show status of each dependency
- Highlight blocked issues
- Calculate total duration
```

**US-5.3: Dependency Risk Analysis**
```
As a TPM
I want to identify dependency risks
So that I can proactively address them

Acceptance Criteria:
- Find issues with blocked dependencies
- Calculate delay impact
- Identify critical path issues
- Show issues blocking multiple others
- Alert on high-risk dependencies
- Recommend mitigation actions
```

### Epic 6: Worklog Analytics

**US-6.1: Worklog Summary**
```
As a TPM
I want to see time logged for a milestone
So that I can track actual vs estimated effort

Acceptance Criteria:
- Sum all worklog entries for milestone
- Group by:
  - Issue type (feature, bug)
  - Team member
  - Week
- Show estimated vs actual time
- Calculate variance
- Identify over/under-estimated issues
```

**US-6.2: Team Time Tracking**
```
As a TPM
I want to see time logged per team member
So that I can track utilization

Acceptance Criteria:
- List all team members
- Show hours logged per person
- Calculate utilization % (logged / capacity)
- Show time distribution (features vs bugs)
- Identify over-worked members
- Generate weekly time report
```

**US-6.3: Cost Analysis**
```
As a TPM
I want to calculate project cost based on worklogs
So that I can track budget

Acceptance Criteria:
- Get hourly rates per role (from config)
- Calculate cost per issue
- Calculate total project cost
- Show cost breakdown:
  - By milestone
  - By team member
  - By issue type
- Compare to budget
- Alert if over budget
```

## Technical Requirements

### TR-1: MCP Integration
- Must use Atlassian MCP for advanced Jira features
- Must use RBKS MCP for Confluence and basic Jira
- Must handle authentication for both MCPs
- Must gracefully fallback if Atlassian MCP unavailable

### TR-2: Data Models
```python
class Milestone:
    name: str
    version_id: str
    target_date: date
    issues: List[Issue]
    
class Sprint:
    id: str
    name: str
    start_date: date
    end_date: date
    goal: str
    issues: List[Issue]
    capacity: int  # story points
    
class Issue:
    key: str
    summary: str
    type: str  # feature, bug, task
    status: str
    assignee: str
    estimate: int  # story points
    time_spent: int  # seconds
    time_remaining: int  # seconds
    dependencies: List[IssueLink]
    
class IssueLink:
    type: str  # blocks, depends_on, relates_to
    target_issue: str
    
class Worklog:
    issue_key: str
    author: str
    time_spent: int  # seconds
    started: datetime
    comment: str
```

### TR-3: Performance
- Must handle programs with 500+ issues
- Must cache Jira data to reduce API calls
- Must batch operations where possible
- Must respond within 10 seconds for most queries

### TR-4: Error Handling
- Must validate Jira permissions before operations
- Must handle rate limiting gracefully
- Must provide clear error messages
- Must rollback on partial failures

### TR-5: Security
- Must respect Jira permissions
- Must not expose sensitive data
- Must audit all write operations
- Must use secure credential storage

## Non-Functional Requirements

### NFR-1: Usability
- Slack commands must be intuitive
- Reports must be readable on mobile
- Charts must be accessible (text fallback)
- Help text must be comprehensive

### NFR-2: Reliability
- Must handle Jira API failures gracefully
- Must retry transient failures
- Must maintain data consistency
- Must log all errors

### NFR-3: Maintainability
- Must follow existing agent patterns
- Must have comprehensive tests
- Must document all Jira API usage
- Must version control prompts

### NFR-4: Scalability
- Must support multiple programs
- Must handle concurrent requests
- Must cache aggressively
- Must paginate large result sets

## Success Metrics

1. **Adoption:** 80% of TPMs use Jira Max weekly
2. **Time Savings:** 5+ hours saved per TPM per week
3. **Accuracy:** 95%+ accuracy in schedule imports
4. **Performance:** <10s response time for 90% of queries
5. **Satisfaction:** 4.5+ star rating from users

## Out of Scope (Future Phases)

- Jira board customization
- Custom field management
- Jira workflow automation
- Integration with external tools (GitHub, etc.)
- Predictive analytics (ML-based)
- Resource planning across programs

## Dependencies

### External
- Atlassian MCP server installed and configured
- RBKS MCP server (already available)
- Jira API access with appropriate permissions
- Confluence API access

### Internal
- Agent #1 (Status Summarizer) - for integration
- Agent #2 (Risk Analyzer) - for integration
- Agent #3 (Team Roster) - for workload distribution
- LangGraph workflow - for orchestration
- Bedrock Claude - for AI analysis

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Atlassian MCP not available | High | Low | Implement fallback using RBKS MCP |
| Jira API rate limiting | Medium | Medium | Implement caching and batching |
| Complex dependency graphs | Medium | Medium | Limit depth, provide warnings |
| Schedule parsing errors | High | Medium | Use AI for robust parsing |
| Performance with large datasets | Medium | High | Implement pagination and caching |

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

## Approval

- [ ] Product Owner: _______________
- [ ] Tech Lead: _______________
- [ ] TPM Stakeholders: _______________
- [ ] Date: _______________
