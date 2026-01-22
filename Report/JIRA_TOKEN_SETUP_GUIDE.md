# Jira API Token Setup Guide for Atlassian MCP

## Current Situation

**Problem:** Ring uses **on-premise Jira** (jira.atl.ring.com), not Atlassian Cloud
- RBKS MCP works because it uses `mwinit` authentication (Amazon internal)
- Atlassian MCP requires API tokens (designed for Atlassian Cloud)

**Solution:** Get a Jira API token from Ring IT to use with Atlassian MCP

## Why You Need This

### RBKS MCP (Current - Working ✅)
- Uses Amazon internal authentication (`mwinit`)
- Works with Ring's on-premise Jira
- No token needed
- Limited to Ring/Blink/Key/Sidewalk tools

### Atlassian MCP (Future - Needs Token 🔑)
- Requires Jira API token
- More comprehensive Jira features
- Standard Atlassian tooling
- Works with on-premise Jira if you have token

## Steps to Get Jira Token

### 1. File IT Ticket
You need to request a Jira API token from Ring IT:

**Ticket Details:**
- **Subject:** Request for Jira API Token for Automation
- **Description:**
  ```
  I need a Jira API token to integrate with automation tools for project management.
  
  Purpose: Automate Jira analytics and reporting for TPM workflows
  Jira Instance: jira.atl.ring.com
  User: danissid@amazon.com
  
  Required Permissions:
  - Read access to Jira projects (PODFLAN, RCIT, etc.)
  - Search issues
  - View issue details
  - View project metadata
  
  This will be used with the Atlassian MCP server for AI-powered 
  project analytics and reporting automation.
  ```

### 2. Token Types

Ring IT may provide one of these:

**Option A: Personal Access Token (PAT)**
- Tied to your user account
- Most common for on-premise Jira
- Format: Long alphanumeric string

**Option B: API Token**
- Generated from Jira profile
- Standard Atlassian approach
- Format: Base64 encoded string

**Option C: OAuth Token**
- More complex setup
- Better for production systems
- Requires OAuth app registration

### 3. Once You Have the Token

#### Configure Atlassian MCP

Create/update `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-atlassian"
      ],
      "env": {
        "ATLASSIAN_INSTANCE_URL": "https://jira.atl.ring.com",
        "ATLASSIAN_USERNAME": "danissid@amazon.com",
        "ATLASSIAN_API_TOKEN": "YOUR_TOKEN_HERE",
        "ATLASSIAN_CONFLUENCE_URL": "https://confluence.atl.ring.com"
      }
    }
  }
}
```

#### Test the Connection

```bash
# Test Jira search
python test_atlassian_mcp.py
```

## Comparison: RBKS MCP vs Atlassian MCP

### RBKS MCP (Current Setup)
**Pros:**
- ✅ Already working
- ✅ No token needed (uses mwinit)
- ✅ Integrated with Ring/Blink/Key/Sidewalk
- ✅ Confluence + Jira + Slack + Figma + Bitbucket

**Cons:**
- ❌ Ring-specific only
- ❌ Limited Jira features
- ❌ Custom implementation

### Atlassian MCP (With Token)
**Pros:**
- ✅ Full Atlassian feature set
- ✅ Standard tooling
- ✅ Better maintained
- ✅ More Jira operations
- ✅ Advanced JQL support

**Cons:**
- ❌ Requires API token
- ❌ Setup complexity
- ❌ Only Jira + Confluence (no Slack/Figma/Bitbucket)

## Recommended Approach

### Phase 1: Continue with RBKS MCP (Now)
- Keep using RBKS MCP for Jira Max agent
- It's working and requires no additional setup
- Covers your current needs

### Phase 2: Add Atlassian MCP (After Token)
- Once you get the token, add Atlassian MCP
- Use it for advanced Jira features
- Keep RBKS MCP for Confluence/Slack/etc.

### Phase 3: Hybrid Approach (Best of Both)
```python
class JiraMaxAgent:
    def __init__(self, rbks_client, atlassian_client):
        self.rbks = rbks_client      # For basic operations
        self.atlassian = atlassian_client  # For advanced features
```

## What to Ask IT For

When filing your ticket, specifically request:

1. **Jira API Token** or **Personal Access Token**
2. **Permissions needed:**
   - Browse projects
   - View issues
   - Search issues
   - View project details
   - View user information
3. **Projects to access:**
   - PODFLAN
   - RCIT
   - PODHEXA
   - (Any other projects you work with)

## Security Notes

⚠️ **Important:**
- Never commit tokens to git
- Store tokens in environment variables or secure config
- Use `.gitignore` for config files with tokens
- Rotate tokens periodically
- Don't share tokens in Slack/email

## Testing After Setup

Once you have the token:

```bash
# 1. Configure Atlassian MCP
vim ~/.kiro/settings/mcp.json

# 2. Restart Kiro to load new MCP server

# 3. Test with simple search
# In Kiro chat:
# "Search Jira for PODFLAN issues"

# 4. Test with Python
cd tpm-slack-bot
python test_atlassian_mcp.py
```

## Next Steps

1. ✅ File IT ticket for Jira API token
2. ⏳ Wait for token (usually 1-3 business days)
3. 🔧 Configure Atlassian MCP with token
4. 🧪 Test connection
5. 🚀 Integrate with Jira Max agent

## Questions to Ask IT

If IT asks for more details:

**Q: Why do you need this?**
A: "I'm building automation tools for TPM workflows that need to analyze Jira data programmatically. This will help with project status reporting, risk analysis, and team workload tracking."

**Q: What will you do with it?**
A: "Read-only access to Jira issues for analytics and reporting. No write operations needed initially."

**Q: Is this for production?**
A: "This is for internal tooling and automation. It will run on my local machine and potentially in AWS Lambda for the TPM Slack bot."

## Current Status

- ✅ RBKS MCP working with mwinit auth
- ✅ Jira Max agent built and ready
- ⏳ Waiting for Jira API token from IT
- ⏳ Atlassian MCP setup pending token

## Contact

If you have issues:
- IT Support: File ticket via internal portal
- Jira Admin: Check with your Jira project admin
- Security: If token permissions are blocked
