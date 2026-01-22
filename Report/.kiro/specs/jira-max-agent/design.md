# Jira Max Agent - Design Document

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Slack Interface                          │
│  /jira-max status DVT | /jira-max sprint create | etc.      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  LangGraph Orchestrator                      │
│  (Routes to appropriate agent based on intent)               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Jira Max Agent                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Intent Classifier (Claude AI)                       │   │
│  │  - milestone_status                                  │   │
│  │  - sprint_planning                                   │   │
│  │  - issue_analytics                                   │   │
│  │  - dependency_analysis                               │   │
│  │  - worklog_tracking                                  │   │
│  │  - schedule_import                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                     │                                        │
│                     ▼                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Sub-Agent Router                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│         │         │         │         │         │           │
│         ▼         ▼         ▼         ▼         ▼           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │Milestone │ │  Sprint  │ │  Issue   │ │Dependency│      │
│  │ Manager  │ │ Planner  │ │ Analyzer │ │ Tracker  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│         │         │         │         │                     │
│         └─────────┴─────────┴─────────┘                     │
│                     │                                        │
│                     ▼                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Data Aggregator & Analyzer (Claude AI)             │   │
│  │  - Combines data from multiple sources               │   │
│  │  - Performs AI analysis                              │   │
│  │  - Generates insights and recommendations            │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘

                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────────┐    ┌──────────────────┐
│  Atlassian MCP   │    │    RBKS MCP      │
│  ┌────────────┐  │    │  ┌────────────┐  │
│  │ Jira       │  │    │  │ Jira       │  │
│  │ - Sprints  │  │    │  │ - Search   │  │
│  │ - Links    │  │    │  │ - Get      │  │
│  │ - Versions │  │    │  │ - Create   │  │
│  │ - Worklogs │  │    │  │ - Update   │  │
│  │ - Batch    │  │    │  └────────────┘  │
│  └────────────┘  │    │  ┌────────────┐  │
│                  │    │  │ Confluence │  │
│                  │    │  │ - Schedules│  │
│                  │    │  └────────────┘  │
└──────────────────┘    └──────────────────┘
```

## Component Design

### 1. Jira Max Agent (Main)

**File:** `tpm-slack-bot/src/agents/jira_max.py`

**Responsibilities:**
- Intent classification
- Sub-agent routing
- Result aggregation
- AI-powered analysis

**Key Methods:**

```python
class JiraMaxAgent(BaseAgent):
    """Advanced Jira project management agent."""
    
    def __init__(self, rbks_client, atlassian_client, 
                 confluence_fetcher, bedrock_client):
        self.rbks_client = rbks_client
        self.atlassian_client = atlassian_client
        self.confluence_fetcher = confluence_fetcher
        self.bedrock_client = bedrock_client
        
        # Sub-agents
        self.milestone_manager = MilestoneManager(...)
        self.sprint_planner = SprintPlanner(...)
        self.issue_analyzer = IssueAnalyzer(...)
        self.dependency_tracker = DependencyTracker(...)
        self.worklog_analyzer = WorklogAnalyzer(...)
        self.schedule_importer = ScheduleImporter(...)
    
    def execute(self, state: TPMState) -> TPMState:
        """Execute based on user query."""
        intent = self._classify_intent(state['user_query'])
        
        if intent == 'milestone_status':
            result = self.milestone_manager.get_status(...)
        elif intent == 'sprint_planning':
            result = self.sprint_planner.create_sprint(...)
        elif intent == 'issue_analytics':
            result = self.issue_analyzer.analyze(...)
        # ... etc
        
        state['agent_results']['jira_max'] = result
        return state
```

### 2. Milestone Manager Sub-Agent

**File:** `tpm-slack-bot/src/agents/jira_max/milestone_manager.py`

**Capabilities:**
- Milestone status tracking
- Features vs bugs analysis
- Worklog summaries
- Risk identification


**Key Methods:**
```python
def get_status(self, program_name: str, milestone_name: str) -> dict:
    """Get comprehensive milestone status."""
    # 1. Get milestone version from Jira
    version = self._get_version(program_name, milestone_name)
    
    # 2. Get all issues for this version
    issues = self._get_version_issues(version.id)
    
    # 3. Calculate progress
    progress = self._calculate_progress(issues)
    
    # 4. Analyze features vs bugs
    features_bugs = self._analyze_features_bugs(issues)
    
    # 5. Get worklog summary
    worklog = self._get_worklog_summary(issues)
    
    # 6. Identify risks
    risks = self._identify_risks(issues)
    
    return {
        'milestone': milestone_name,
        'target_date': version.release_date,
        'days_remaining': (version.release_date - date.today()).days,
        'progress': progress,
        'features_vs_bugs': features_bugs,
        'worklog': worklog,
        'risks': risks
    }
```

### 3. Sprint Planner Sub-Agent

**File:** `tpm-slack-bot/src/agents/jira_max/sprint_planner.py`

**Capabilities:**
- Sprint creation
- Workload balancing
- Capacity planning
- Sprint status tracking


**Key Methods:**
```python
def create_sprint(self, program_name: str, milestone_name: str, 
                 team_capacity: int) -> dict:
    """Create a new sprint for a milestone."""
    # 1. Get board for program
    board = self._get_board(program_name)
    
    # 2. Get unassigned issues for milestone
    issues = self._get_unassigned_issues(program_name, milestone_name)
    
    # 3. Select issues that fit capacity
    selected_issues = self._select_issues_for_capacity(issues, team_capacity)
    
    # 4. Balance workload across team (AI-powered)
    assignments = self._balance_workload(selected_issues)
    
    # 5. Create sprint in Jira
    sprint = self._create_sprint_in_jira(board.id, milestone_name)
    
    # 6. Add issues to sprint
    self._add_issues_to_sprint(sprint.id, selected_issues)
    
    # 7. Assign issues to team members
    self._assign_issues(assignments)
    
    return sprint_summary
```

### 4. Issue Analyzer Sub-Agent

**File:** `tpm-slack-bot/src/agents/jira_max/issue_analyzer.py`

**Capabilities:**
- Time-to-close analysis
- Velocity tracking
- Bottleneck identification
- Performance metrics


### 5. Dependency Tracker Sub-Agent

**File:** `tpm-slack-bot/src/agents/jira_max/dependency_tracker.py`

**Capabilities:**
- Create issue links
- Visualize dependency chains
- Identify critical paths
- Risk analysis

### 6. Worklog Analyzer Sub-Agent

**File:** `tpm-slack-bot/src/agents/jira_max/worklog_analyzer.py`

**Capabilities:**
- Time tracking summaries
- Actual vs estimated analysis
- Team utilization tracking
- Cost calculations

### 7. Schedule Importer Sub-Agent

**File:** `tpm-slack-bot/src/agents/jira_max/schedule_importer.py`

**Capabilities:**
- Parse Confluence schedules
- Create Jira versions
- Create issues from schedule
- Set up dependencies

## MCP Integration Strategy

### Atlassian MCP (Primary)

**Used For:**
- Sprint management (create, update, get sprints)
- Issue links (create dependencies)
- Worklogs (get time tracking data)
- Versions (milestone management)
- Batch operations (bulk updates)

**Tools:**
- `jira_get_sprints`
- `jira_create_sprint`
- `jira_add_issues_to_sprint`
- `jira_get_worklog`
- `jira_create_issue_link`
- `jira_get_project_versions`


### RBKS MCP (Fallback & Confluence)

**Used For:**
- Basic Jira operations (search, get, create, update)
- Confluence access (schedule parsing)
- Fallback when Atlassian MCP unavailable

**Tools:**
- `jira_search_issues`
- `jira_get_issue`
- `jira_create_issue`
- `jira_update_issue`
- `confluence_get_page`
- `confluence_search_pages`

### Dual MCP Pattern

```python
class JiraMaxAgent:
    def _get_sprints(self, board_id: str):
        """Get sprints with fallback."""
        try:
            # Try Atlassian MCP first (more features)
            return self.atlassian_client.get_sprints(board_id)
        except Exception as e:
            logger.warning(f"Atlassian MCP failed: {e}")
            # Fallback to RBKS MCP
            return self._get_sprints_via_search()
    
    def _get_sprints_via_search(self):
        """Fallback using RBKS MCP search."""
        # Use JQL to find sprint information
        jql = 'sprint is not EMPTY'
        issues = self.rbks_client.search_issues(jql)
        # Extract sprint info from issues
        return self._extract_sprint_info(issues)
```

## Data Flow Examples

### Example 1: Milestone Status Report

```
User: "Show me DVT milestone status"
  ↓
LangGraph Orchestrator
  ↓
Jira Max Agent (classify intent: milestone_status)
  ↓
Milestone Manager
  ↓
1. Get version via Atlassian MCP
2. Search issues via RBKS MCP
3. Get worklogs via Atlassian MCP
4. Analyze with Claude AI
  ↓
Format response
  ↓
Return to Slack
```


### Example 2: Create Sprint

```
User: "Create sprint for DVT with 80 points capacity"
  ↓
LangGraph Orchestrator
  ↓
Jira Max Agent (classify intent: sprint_planning)
  ↓
Sprint Planner
  ↓
1. Get board via Atlassian MCP
2. Search unassigned issues via RBKS MCP
3. Select issues (AI-powered)
4. Create sprint via Atlassian MCP
5. Add issues via Atlassian MCP
6. Assign issues via RBKS MCP
  ↓
Format response
  ↓
Return to Slack
```

### Example 3: Import Schedule

```
User: "Import schedule from Confluence page 123456"
  ↓
LangGraph Orchestrator
  ↓
Jira Max Agent (classify intent: schedule_import)
  ↓
Schedule Importer
  ↓
1. Get Confluence page via RBKS MCP
2. Parse schedule (AI-powered)
3. Create versions via Atlassian MCP
4. Create issues via RBKS MCP (batch)
5. Create dependencies via Atlassian MCP
  ↓
Format response
  ↓
Return to Slack
```

## AI Integration Points

### 1. Intent Classification
**Model:** Claude 3.5 Sonnet
**Purpose:** Classify user query into sub-agent category
**Input:** User query text
**Output:** Intent category + extracted parameters


### 2. Schedule Parsing
**Model:** Claude 3.5 Sonnet
**Purpose:** Extract structured data from Confluence schedules
**Input:** Confluence page HTML/markdown
**Output:** Structured schedule data (milestones, tasks, dates)

### 3. Workload Balancing
**Model:** Claude 3.5 Sonnet
**Purpose:** Intelligently assign issues to team members
**Input:** Issues, team members, skills, current workload
**Output:** Optimal assignments

### 4. Risk Analysis
**Model:** Claude 3.5 Sonnet
**Purpose:** Identify and prioritize risks
**Input:** Issue data, dependencies, timelines
**Output:** Risk list with severity and recommendations

### 5. Insight Generation
**Model:** Claude 3.5 Sonnet
**Purpose:** Generate actionable insights from metrics
**Input:** Metrics, trends, historical data
**Output:** Natural language insights and recommendations

## Caching Strategy

### Level 1: In-Memory Cache
- TTL: 5 minutes
- Data: Frequently accessed issues, sprints, versions
- Implementation: Python dict with timestamps

### Level 2: Redis Cache (Future)
- TTL: 1 hour
- Data: Issue search results, worklog summaries
- Implementation: Redis with JSON serialization

### Cache Invalidation
- On issue update: Clear issue cache
- On sprint update: Clear sprint cache
- On version update: Clear version cache
- Manual: `/jira-max cache clear`

## Error Handling

### MCP Failures
```python
try:
    result = self.atlassian_client.get_sprints(board_id)
except MCPConnectionError:
    # Fallback to RBKS MCP
    result = self._get_sprints_fallback()
except MCPAuthError:
    # Return error to user
    return "Authentication failed. Please check MCP config."
```


### Rate Limiting
```python
@retry(max_attempts=3, backoff=exponential)
def _call_jira_api(self, method, *args, **kwargs):
    """Call Jira API with rate limiting."""
    if self._is_rate_limited():
        time.sleep(self._get_backoff_time())
    return method(*args, **kwargs)
```

### Partial Failures
```python
def create_issues_batch(self, issues: List[dict]) -> dict:
    """Create multiple issues with rollback on failure."""
    created = []
    try:
        for issue in issues:
            created_issue = self._create_issue(issue)
            created.append(created_issue)
        return {'success': True, 'created': created}
    except Exception as e:
        # Rollback created issues
        for issue in created:
            self._delete_issue(issue.key)
        return {'success': False, 'error': str(e)}
```

## Performance Optimization

### Batch Operations
- Create multiple issues in single request
- Update multiple issues in parallel
- Fetch related data in single query

### Pagination
- Limit search results to 100 per page
- Use cursor-based pagination for large datasets
- Stream results for real-time updates

### Parallel Processing
```python
async def get_milestone_data(self, milestone_name: str):
    """Fetch milestone data in parallel."""
    tasks = [
        self._get_version(milestone_name),
        self._get_issues(milestone_name),
        self._get_worklogs(milestone_name)
    ]
    version, issues, worklogs = await asyncio.gather(*tasks)
    return self._combine_data(version, issues, worklogs)
```

## Security Considerations

### Permission Checks
```python
def _check_permissions(self, user_id: str, project_key: str):
    """Verify user has access to project."""
    user_projects = self._get_user_projects(user_id)
    if project_key not in user_projects:
        raise PermissionError(f"No access to {project_key}")
```


### Audit Logging
```python
def _audit_log(self, action: str, user_id: str, details: dict):
    """Log all write operations."""
    log_entry = {
        'timestamp': datetime.now(),
        'action': action,
        'user_id': user_id,
        'details': details
    }
    self.audit_logger.info(json.dumps(log_entry))
```

### Data Sanitization
- Remove sensitive data from logs
- Mask user emails in responses
- Validate all user inputs

## Testing Strategy

### Unit Tests
- Test each sub-agent independently
- Mock MCP clients
- Test error handling
- Test caching logic

### Integration Tests
- Test with real MCP servers
- Test fallback mechanisms
- Test end-to-end workflows
- Test performance under load

### Test Coverage Goals
- Unit tests: 80%+
- Integration tests: Key workflows
- Performance tests: Response time < 10s

## Monitoring & Observability

### Metrics
- Request count per sub-agent
- Response time per operation
- MCP call count and latency
- Cache hit/miss ratio
- Error rate by type

### Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Include request ID for tracing
- Log MCP calls and responses

### Alerts
- High error rate (>5%)
- Slow response time (>10s)
- MCP connection failures
- Cache failures

## Deployment

### Prerequisites
- Atlassian MCP server configured
- RBKS MCP server configured
- Bedrock access configured
- Redis (optional, for caching)

### Configuration
```yaml
jira_max:
  atlassian_mcp:
    enabled: true
    fallback_to_rbks: true
  cache:
    enabled: true
    ttl_seconds: 300
  performance:
    max_issues_per_query: 500
    batch_size: 50
  features:
    schedule_import: true
    dependency_tracking: true
    worklog_analysis: true
```

### Rollout Plan
1. Deploy to dev environment
2. Test with sample data
3. Deploy to staging
4. Beta test with 2-3 TPMs
5. Collect feedback
6. Deploy to production
7. Monitor for 1 week
8. Full rollout

## Future Enhancements

### Phase 3
- Predictive analytics (ML-based)
- Custom dashboards
- Automated reporting
- Integration with GitHub

### Phase 4
- Resource planning across programs
- Budget forecasting
- Team capacity planning
- Advanced visualizations
