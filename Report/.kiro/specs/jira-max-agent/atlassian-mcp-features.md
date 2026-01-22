# Atlassian MCP Features for Jira Max

## Overview

This document details the additional features provided by the Atlassian MCP (https://github.com/sooperset/mcp-atlassian) that are not available in RBKS MCP, and how Jira Max will leverage them.

## Key Differentiators

### 1. Sprint Management

**Atlassian MCP Tools:**
- `jira_get_sprints` - Get all sprints for a board
- `jira_create_sprint` - Create a new sprint
- `jira_update_sprint` - Update sprint details
- `jira_start_sprint` - Start a sprint
- `jira_close_sprint` - Close a sprint
- `jira_add_issues_to_sprint` - Add issues to a sprint
- `jira_remove_issues_from_sprint` - Remove issues from a sprint

**RBKS MCP Limitation:**
- No direct sprint management
- Must use workarounds via JQL queries

**Jira Max Usage:**
- Sprint creation for milestones (US-3.1)
- Sprint status tracking (US-3.2)
- Workload distribution (US-3.3)

### 2. Issue Links (Dependencies)

**Atlassian MCP Tools:**
- `jira_create_issue_link` - Create dependency between issues
- `jira_get_issue_links` - Get all links for an issue
- `jira_delete_issue_link` - Remove a link

**Link Types Supported:**
- Blocks / Is blocked by
- Depends on / Is depended on by
- Relates to
- Duplicates / Is duplicated by
- Clones / Is cloned by

**RBKS MCP Limitation:**
- No direct link management
- Links only visible in issue details

**Jira Max Usage:**
- Create dependencies (US-5.1)
- Dependency visualization (US-5.2)
- Dependency risk analysis (US-5.3)
- Schedule import with dependencies (US-1.1)

### 3. Worklog Management

**Atlassian MCP Tools:**
- `jira_get_worklog` - Get all worklogs for an issue
- `jira_add_worklog` - Add time tracking entry
- `jira_update_worklog` - Update worklog entry
- `jira_delete_worklog` - Delete worklog entry

**Worklog Data:**
- Time spent (seconds)
- Author
- Started timestamp
- Comment/description

**RBKS MCP Limitation:**
- No worklog access
- Cannot track time spent

**Jira Max Usage:**
- Worklog summaries (US-2.1, US-6.1)
- Team time tracking (US-6.2)
- Cost analysis (US-6.3)
- Actual vs estimated analysis

### 4. Version Management

**Atlassian MCP Tools:**
- `jira_get_project_versions` - Get all versions/milestones
- `jira_create_version` - Create a new version
- `jira_update_version` - Update version details
- `jira_delete_version` - Delete a version

**Version Data:**
- Name
- Description
- Release date
- Released status
- Archived status

**RBKS MCP Limitation:**
- No version management
- Must use JQL to filter by version

**Jira Max Usage:**
- Milestone tracking (US-2.1, US-2.2)
- Schedule import (US-1.1)
- Version creation for milestones

### 5. Batch Operations

**Atlassian MCP Tools:**
- `jira_bulk_create_issues` - Create multiple issues at once
- `jira_bulk_update_issues` - Update multiple issues at once
- `jira_bulk_transition_issues` - Transition multiple issues

**RBKS MCP Limitation:**
- Must create/update issues one at a time
- Slower for large operations

**Jira Max Usage:**
- Schedule import (US-1.1) - Create many issues
- Sprint planning (US-3.1) - Assign many issues
- Bulk status updates

### 6. Board Management

**Atlassian MCP Tools:**
- `jira_get_boards` - Get all boards
- `jira_get_board` - Get board details
- `jira_get_board_configuration` - Get board settings

**Board Data:**
- Board ID
- Board name
- Board type (Scrum, Kanban)
- Filter ID
- Columns

**RBKS MCP Limitation:**
- No board access
- Cannot get board configuration

**Jira Max Usage:**
- Sprint creation (US-3.1) - Need board ID
- Sprint status (US-3.2) - Board-based queries

## Fallback Strategy

When Atlassian MCP is unavailable, Jira Max will fallback to RBKS MCP with reduced functionality:

### Sprint Management Fallback
```python
# Instead of: atlassian_client.get_sprints(board_id)
# Use: JQL query to extract sprint info from issues
jql = 'sprint is not EMPTY AND project = RCIT'
issues = rbks_client.search_issues(jql)
sprints = extract_sprint_info_from_issues(issues)
```

### Worklog Fallback
```python
# Instead of: atlassian_client.get_worklog(issue_key)
# Use: Issue time tracking fields
issue = rbks_client.get_issue(issue_key)
time_spent = issue.fields.timespent  # Total only, no breakdown
```

### Version Fallback
```python
# Instead of: atlassian_client.get_project_versions(project_key)
# Use: JQL query to find versions
jql = 'project = RCIT AND fixVersion is not EMPTY'
issues = rbks_client.search_issues(jql)
versions = extract_versions_from_issues(issues)
```

### Link Fallback
```python
# Instead of: atlassian_client.create_issue_link(...)
# Use: Manual tracking in issue description or comments
# Limited functionality - cannot create actual links
```

## Configuration

```yaml
jira_max:
  atlassian_mcp:
    enabled: true
    url: "http://localhost:3000"
    fallback_to_rbks: true
  
  features:
    # Require Atlassian MCP
    sprint_management: true
    dependency_tracking: true
    worklog_analysis: true
    
    # Work with RBKS MCP fallback
    milestone_tracking: true
    issue_analytics: true
    schedule_import: true  # Limited without links
```

## Testing

### With Atlassian MCP
```bash
# Test sprint creation
python cli_test_jira_max.py --test sprint_create

# Test worklog analysis
python cli_test_jira_max.py --test worklog_summary

# Test dependency creation
python cli_test_jira_max.py --test create_dependencies
```

### Without Atlassian MCP (Fallback)
```bash
# Test with RBKS MCP only
python cli_test_jira_max.py --no-atlassian --test milestone_status

# Verify graceful degradation
python cli_test_jira_max.py --no-atlassian --test sprint_create
# Should show: "Sprint management requires Atlassian MCP"
```

## Performance Comparison

| Operation | Atlassian MCP | RBKS MCP Fallback |
|-----------|---------------|-------------------|
| Get sprints | 1 API call | 10+ API calls (via JQL) |
| Create sprint | 1 API call | Not possible |
| Get worklogs | 1 API call per issue | Not available |
| Create links | 1 API call per link | Not possible |
| Bulk create issues | 1 API call | N API calls |

## Recommendation

**For Production:** Install and configure Atlassian MCP for full functionality.

**For Development:** Can use RBKS MCP only for basic testing, but many features will be limited.

**For Demo:** Use Atlassian MCP to showcase all capabilities.
