# Atlassian MCP Setup Guide

## Overview

This guide walks through setting up the Atlassian MCP server (https://github.com/sooperset/mcp-atlassian) for use with Jira Max agent.

## Prerequisites

- Node.js 18+ installed
- Jira Cloud or Server access
- Jira API token or credentials
- Confluence access (optional, for schedule import)

## Installation

### Option 1: NPM Global Install (Recommended)

```bash
npm install -g @sooperset/mcp-atlassian
```

### Option 2: Clone and Build

```bash
git clone https://github.com/sooperset/mcp-atlassian.git
cd mcp-atlassian
npm install
npm run build
```

## Configuration

### 1. Create MCP Configuration

Add to your Kiro MCP config (`.kiro/settings/mcp.json`):

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": ["-y", "@sooperset/mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-domain.atlassian.net",
        "JIRA_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "your-api-token",
        "CONFLUENCE_URL": "https://your-domain.atlassian.net/wiki",
        "CONFLUENCE_EMAIL": "your-email@company.com",
        "CONFLUENCE_API_TOKEN": "your-api-token"
      },
      "disabled": false,
      "autoApprove": [
        "jira_search_issues",
        "jira_get_issue",
        "jira_get_sprints",
        "jira_get_worklog",
        "jira_get_issue_links",
        "jira_get_project_versions"
      ]
    }
  }
}
```

### 2. Get Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "Jira Max MCP")
4. Copy the token
5. Add to MCP config as `JIRA_API_TOKEN`

### 3. Get Confluence API Token

1. Same as Jira (Atlassian uses same token system)
2. Or use the same token as Jira
3. Add to MCP config as `CONFLUENCE_API_TOKEN`

## Verification

### 1. Test MCP Connection

```bash
# In Kiro, open command palette
# Search for "MCP: Reconnect Servers"
# Check that "atlassian" server connects successfully
```

### 2. Test Basic Operations

Create a test file `test_atlassian_mcp.py`:

```python
from src.services.mcp_client import MCPClient

# Initialize MCP client
mcp = MCPClient()

# Test 1: Get sprints
print("Testing get_sprints...")
sprints = mcp.call_tool("atlassian", "jira_get_sprints", {
    "boardId": "123"  # Replace with your board ID
})
print(f"Found {len(sprints)} sprints")

# Test 2: Get worklogs
print("\nTesting get_worklog...")
worklogs = mcp.call_tool("atlassian", "jira_get_worklog", {
    "issueKey": "RCIT-1234"  # Replace with your issue key
})
print(f"Found {len(worklogs)} worklog entries")

# Test 3: Get versions
print("\nTesting get_project_versions...")
versions = mcp.call_tool("atlassian", "jira_get_project_versions", {
    "projectKey": "RCIT"  # Replace with your project key
})
print(f"Found {len(versions)} versions")

# Test 4: Get issue links
print("\nTesting get_issue_links...")
links = mcp.call_tool("atlassian", "jira_get_issue_links", {
    "issueKey": "RCIT-1234"  # Replace with your issue key
})
print(f"Found {len(links)} links")

print("\n✅ All tests passed!")
```

Run the test:

```bash
cd tpm-slack-bot
python test_atlassian_mcp.py
```

## Available Tools

### Sprint Management
- `jira_get_sprints` - Get all sprints for a board
- `jira_create_sprint` - Create a new sprint
- `jira_update_sprint` - Update sprint details
- `jira_start_sprint` - Start a sprint
- `jira_close_sprint` - Close a sprint
- `jira_add_issues_to_sprint` - Add issues to sprint
- `jira_remove_issues_from_sprint` - Remove issues from sprint

### Issue Links
- `jira_create_issue_link` - Create dependency
- `jira_get_issue_links` - Get all links for issue
- `jira_delete_issue_link` - Remove a link

### Worklog
- `jira_get_worklog` - Get all worklogs for issue
- `jira_add_worklog` - Add time tracking entry
- `jira_update_worklog` - Update worklog entry
- `jira_delete_worklog` - Delete worklog entry

### Versions
- `jira_get_project_versions` - Get all versions
- `jira_create_version` - Create a new version
- `jira_update_version` - Update version details
- `jira_delete_version` - Delete a version

### Boards
- `jira_get_boards` - Get all boards
- `jira_get_board` - Get board details
- `jira_get_board_configuration` - Get board settings

### Batch Operations
- `jira_bulk_create_issues` - Create multiple issues
- `jira_bulk_update_issues` - Update multiple issues
- `jira_bulk_transition_issues` - Transition multiple issues

## Troubleshooting

### Issue: "Connection refused"

**Solution:**
1. Check that Node.js is installed: `node --version`
2. Check that npx is available: `npx --version`
3. Try manual install: `npm install -g @sooperset/mcp-atlassian`

### Issue: "Authentication failed"

**Solution:**
1. Verify API token is correct
2. Verify email matches Jira account
3. Check that token has not expired
4. Try creating a new API token

### Issue: "Board not found"

**Solution:**
1. Get board ID from Jira URL: `https://your-domain.atlassian.net/jira/software/c/projects/RCIT/boards/123`
2. Board ID is the number at the end (123)
3. Verify you have access to the board

### Issue: "Rate limit exceeded"

**Solution:**
1. Implement caching in Jira Max agent
2. Reduce frequency of API calls
3. Use batch operations where possible
4. Contact Atlassian support to increase limits

## Integration with Jira Max

### 1. Update MCP Client

Add Atlassian MCP support to `src/services/mcp_client.py`:

```python
class MCPClient:
    def __init__(self):
        self.rbks_server = "rbks-mcp-servers"
        self.atlassian_server = "atlassian"
    
    def get_sprints(self, board_id: str):
        """Get sprints with fallback."""
        try:
            return self.call_tool(self.atlassian_server, "jira_get_sprints", {
                "boardId": board_id
            })
        except Exception as e:
            logger.warning(f"Atlassian MCP failed: {e}, falling back to RBKS")
            return self._get_sprints_fallback(board_id)
```

### 2. Create Atlassian Client Wrapper

Create `src/services/atlassian_mcp_client.py`:

```python
class AtlassianMCPClient:
    """Wrapper for Atlassian MCP operations."""
    
    def __init__(self, mcp_client: MCPClient):
        self.mcp = mcp_client
        self.server = "atlassian"
    
    def get_sprints(self, board_id: str):
        return self.mcp.call_tool(self.server, "jira_get_sprints", {
            "boardId": board_id
        })
    
    def create_sprint(self, board_id: str, name: str, start_date: str, end_date: str):
        return self.mcp.call_tool(self.server, "jira_create_sprint", {
            "boardId": board_id,
            "name": name,
            "startDate": start_date,
            "endDate": end_date
        })
    
    # ... more methods
```

### 3. Use in Jira Max Agent

```python
from src.services.atlassian_mcp_client import AtlassianMCPClient

class JiraMaxAgent:
    def __init__(self, rbks_client, mcp_client, ...):
        self.rbks_client = rbks_client
        self.atlassian_client = AtlassianMCPClient(mcp_client)
        # ...
```

## Security Best Practices

1. **Never commit API tokens** to git
2. **Use environment variables** for sensitive data
3. **Rotate tokens regularly** (every 90 days)
4. **Use separate tokens** for dev/staging/prod
5. **Limit token permissions** to minimum required
6. **Monitor token usage** for suspicious activity

## Performance Tips

1. **Cache aggressively** - Sprints, versions, boards rarely change
2. **Batch operations** - Use bulk APIs when possible
3. **Parallel requests** - Fetch independent data concurrently
4. **Pagination** - Limit results to what's needed
5. **Rate limiting** - Implement exponential backoff

## Next Steps

1. ✅ Install Atlassian MCP
2. ✅ Configure authentication
3. ✅ Test basic operations
4. ✅ Integrate with Jira Max agent
5. ⏭️ Start implementing Phase 2A (Basic Analytics)

## Support

- **Atlassian MCP Issues:** https://github.com/sooperset/mcp-atlassian/issues
- **Jira API Docs:** https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **Confluence API Docs:** https://developer.atlassian.com/cloud/confluence/rest/v2/
