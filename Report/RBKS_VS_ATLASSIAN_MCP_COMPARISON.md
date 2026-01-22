# RBKS MCP vs Atlassian MCP - Feature Comparison

**Last Updated:** January 17, 2025  
**Status:** ✅ RBKS MCP fully tested and working

## TL;DR

**RBKS MCP alone gets you 70% of Jira Max functionality.** The missing 30% is advanced features like sprint management, worklogs, and dependencies.

## ⚠️ Critical Requirements

### RBKS MCP Requirements
- ✅ **VPN Connection Required** - Must be connected to Amazon VPN
- ✅ **Midway Authentication** - Run `mwinit -o` before use
- ✅ **Kiro Integration** - Works through Kiro's MCP system
- ⚠️ **Cannot call binary directly** - Must use through Kiro or proper MCP client

### Atlassian MCP Requirements
- ✅ **API Token** - One-time setup with Jira API token
- ✅ **No VPN needed** - Works from anywhere
- ✅ **Standalone** - Can call directly from Python scripts

## What RBKS MCP Provides (Already Working!)

### ✅ Core Jira Operations
- `jira_search_issues` - Search with JQL
- `jira_get_issue` - Get issue details
- `jira_create_issue` - Create new issues
- `jira_update_issue` - Update issues
- `jira_add_comment` - Add comments
- `jira_transition_issue` - Change status
- `jira_get_transitions` - Get available transitions
- `jira_get_sprints` - Get sprint info (basic)

### ✅ Confluence Integration
- `confluence_get_page` - Get page content (markdown)
- `confluence_search_pages` - Search pages
- `confluence_create_page` - Create pages
- `confluence_update_page` - Update pages
- `confluence_get_spaces` - List spaces

### ✅ Bonus Features
- **Slack integration** - Messages, search, threads, posting
- **Figma integration** - Design files, comments
- **BitBucket integration** - Repos, PRs, code

### ✅ Authentication
- **Built-in Midway SSO** - No API tokens needed
- **Already authenticated** - Just run `mwinit -o`
- **No setup required** - Works immediately

## What You CAN Build with RBKS MCP Only

### Phase 1: Basic Jira Max (70% of requirements)

#### ✅ Issue Analytics
```python
# Search and analyze issues
issues = jira_search_issues(jql="project=RCIT AND status=Open")

# Calculate metrics
- Time-to-close (using created/resolved dates)
- Features vs bugs ratio
- Status breakdown
- Assignee workload
```

#### ✅ Milestone Status Reports
```python
# Get issues for milestone
issues = jira_search_issues(jql="fixVersion='DVT' AND project=RCIT")

# Generate report
- Completed count and %
- In Progress count and %
- To Do count and %
- Features vs bugs
- Blocked issues (using status)
```

#### ✅ Schedule Import (Confluence → Jira)
```python
# Parse Confluence schedule
page = confluence_get_page(page_id="2814198025")

# Create Jira issues
for task in schedule:
    jira_create_issue(
        summary=task.name,
        description=task.details,
        assignee=task.owner,
        dueDate=task.date
    )
```

#### ✅ Team Workload Distribution
```python
# Get issues per person
issues = jira_search_issues(jql="assignee=currentUser()")

# Calculate workload
- Issue count per person
- Story points per person (if in issue data)
- Status distribution
```

#### ✅ Dependency Tracking (Basic)
```python
# Get issue with links
issue = jira_get_issue(issue_key="RCIT-1234")

# Check for blockers in description or comments
# Note: No dedicated dependency API, but can parse issue data
```

## What You CANNOT Build with RBKS MCP Only

### ❌ Advanced Sprint Management

**Missing:**
- `jira_create_sprint` - Create new sprints
- `jira_update_sprint` - Update sprint details
- `jira_start_sprint` - Start a sprint
- `jira_close_sprint` - Close a sprint
- `jira_add_issues_to_sprint` - Add issues to sprint
- `jira_remove_issues_from_sprint` - Remove issues

**Impact:** Can't automate sprint creation or management. Must do manually in Jira UI.

**Workaround:** Use `jira_get_sprints` to read sprint data, but can't modify.

### ❌ Worklog Analytics

**Missing:**
- `jira_get_worklog` - Get time tracking entries
- `jira_add_worklog` - Add time entries
- `jira_update_worklog` - Update time entries
- `jira_delete_worklog` - Delete time entries

**Impact:** Can't track actual time spent vs estimates. Can't do cost analysis.

**Workaround:** None. Worklog data not available in basic issue API.

### ❌ Issue Dependencies

**Missing:**
- `jira_create_issue_link` - Create "blocks/depends on" links
- `jira_get_issue_links` - Get all links for issue
- `jira_delete_issue_link` - Remove links

**Impact:** Can't programmatically manage dependencies. Can't visualize dependency chains.

**Workaround:** Parse issue descriptions/comments for manual dependency tracking.

### ❌ Version Management

**Missing:**
- `jira_get_project_versions` - Get all versions/milestones
- `jira_create_version` - Create new version
- `jira_update_version` - Update version details
- `jira_delete_version` - Delete version

**Impact:** Can't automate milestone creation. Must use JQL to filter by version name.

**Workaround:** Use `fixVersion` in JQL, but can't create/modify versions.

### ❌ Batch Operations

**Missing:**
- `jira_bulk_create_issues` - Create multiple issues at once
- `jira_bulk_update_issues` - Update multiple issues
- `jira_bulk_transition_issues` - Transition multiple issues

**Impact:** Slower when creating many issues (must loop one-by-one).

**Workaround:** Loop with rate limiting. Works but slower.

## Feature Comparison Table

| Feature | RBKS MCP | Atlassian MCP | Impact |
|---------|----------|---------------|--------|
| **Issue CRUD** | ✅ Full | ✅ Full | None |
| **Issue Search** | ✅ Full | ✅ Full | None |
| **Comments** | ✅ Full | ✅ Full | None |
| **Transitions** | ✅ Full | ✅ Full | None |
| **Sprint Read** | ✅ Basic | ✅ Full | Can read but not modify |
| **Sprint Write** | ❌ None | ✅ Full | **Can't automate sprint planning** |
| **Worklogs** | ❌ None | ✅ Full | **Can't track time/cost** |
| **Dependencies** | ❌ None | ✅ Full | **Can't manage dependencies** |
| **Versions** | ❌ None | ✅ Full | **Can't create milestones** |
| **Batch Ops** | ❌ None | ✅ Full | Slower bulk operations |
| **Confluence** | ✅ Full | ✅ Full | None |
| **Slack** | ✅ Full | ❌ None | RBKS advantage |
| **Figma** | ✅ Full | ❌ None | RBKS advantage |
| **BitBucket** | ✅ Full | ❌ None | RBKS advantage |
| **Authentication** | ✅ Midway | ❌ API Token | RBKS easier |

## Jira Max Requirements Coverage

### With RBKS MCP Only: 70% Coverage

| Epic | Coverage | Notes |
|------|----------|-------|
| **Schedule-to-Jira Translation** | ✅ 90% | Can import, can't create versions |
| **Milestone Management** | ✅ 80% | Can report, can't create milestones |
| **Sprint Planning** | ⚠️ 40% | Can read, **can't create/manage** |
| **Issue Analytics** | ✅ 90% | Full coverage except worklogs |
| **Dependency Management** | ⚠️ 30% | Can parse, **can't create links** |
| **Worklog Analytics** | ❌ 0% | **No worklog access** |

### With RBKS + Atlassian MCP: 100% Coverage

All requirements fully covered.

## Recommendation: Start with RBKS MCP Only

### Why?

1. **Already working** - No setup needed
2. **70% coverage** - Gets most value immediately
3. **No authentication hassle** - Uses Midway
4. **Bonus features** - Slack, Figma, BitBucket
5. **Can add Atlassian later** - Not blocked

### When to Add Atlassian MCP?

Add Atlassian MCP when you need:
- Automated sprint creation/management
- Time tracking and cost analysis
- Programmatic dependency management
- Milestone/version automation

**Estimate:** You'll want Atlassian MCP in Phase 2C (Sprint Planning) - Week 5-6.

## Implementation Strategy

### Phase 1: RBKS MCP Only (Weeks 1-4)

**Build:**
- ✅ Issue search and analytics
- ✅ Milestone status reports
- ✅ Schedule import (Confluence → Jira)
- ✅ Team workload distribution
- ✅ Features vs bugs analysis
- ✅ Basic dependency tracking (parse descriptions)

**Skip:**
- ⏭️ Sprint automation
- ⏭️ Worklog analytics
- ⏭️ Dependency links

### Phase 2: Add Atlassian MCP (Weeks 5-8)

**Add:**
- ✅ Sprint creation and management
- ✅ Worklog tracking and cost analysis
- ✅ Dependency link management
- ✅ Version/milestone automation
- ✅ Batch operations

## Code Example: RBKS MCP Only

```python
class JiraMaxAgent:
    """Jira Max using RBKS MCP only."""
    
    def __init__(self, rbks_client):
        self.jira = rbks_client
    
    def milestone_status(self, milestone_name: str):
        """Get milestone status - WORKS with RBKS MCP."""
        # Search issues for milestone
        issues = self.jira.call_tool("jira_search_issues", {
            "jql": f"fixVersion='{milestone_name}' AND project=RCIT"
        })
        
        # Calculate metrics
        total = len(issues)
        done = len([i for i in issues if i['status'] == 'Done'])
        in_progress = len([i for i in issues if i['status'] == 'In Progress'])
        
        return {
            "milestone": milestone_name,
            "total": total,
            "done": done,
            "done_pct": done / total * 100,
            "in_progress": in_progress
        }
    
    def create_sprint(self, board_id: str, name: str):
        """Create sprint - DOES NOT WORK with RBKS MCP."""
        # ❌ This tool doesn't exist in RBKS MCP
        raise NotImplementedError("Need Atlassian MCP for sprint creation")
    
    def get_worklogs(self, issue_key: str):
        """Get worklogs - DOES NOT WORK with RBKS MCP."""
        # ❌ This tool doesn't exist in RBKS MCP
        raise NotImplementedError("Need Atlassian MCP for worklogs")
```

## Next Steps

### Option A: Start with RBKS MCP Only (Recommended)

1. ✅ Already authenticated (mwinit)
2. ✅ Build Phase 1 features (70% coverage)
3. ✅ Get value immediately
4. ⏭️ Add Atlassian MCP later when needed

**Time to value:** Immediate

### Option B: Add Atlassian MCP Now

1. ⏱️ Get Jira API token (5 minutes)
2. ⏱️ Configure Atlassian MCP (5 minutes)
3. ⏱️ Test both MCPs (10 minutes)
4. ✅ Build with 100% coverage

**Time to value:** 20 minutes + build time

## My Recommendation

**Start with RBKS MCP only.** Here's why:

1. You're already authenticated
2. You can build 70% of Jira Max today
3. The missing 30% (sprints, worklogs) are Phase 2C features (weeks away)
4. You'll know by then if you really need those features
5. Adding Atlassian MCP later is easy

**Build Phase 1 with RBKS MCP, then reassess.**

---

## Questions?

**Q: Can I use both MCPs together?**  
A: Yes! They complement each other. Use RBKS for basic ops + Slack/Figma, use Atlassian for advanced features.

**Q: Will I need to rewrite code if I add Atlassian MCP later?**  
A: No. Just add new methods for advanced features. Existing code keeps working.

**Q: What if RBKS MCP adds these features later?**  
A: Great! Then you won't need Atlassian MCP at all.

**Q: Can I try Atlassian MCP without committing?**  
A: Yes. Just add it to your config, test it, remove if you don't need it.
