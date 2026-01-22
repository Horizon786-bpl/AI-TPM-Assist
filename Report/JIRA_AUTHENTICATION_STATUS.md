# Jira Authentication Status - BLOCKER IDENTIFIED

## 🔴 Current Blocker: RBKS MCP Authentication

### What's Happening
The RBKS MCP server is returning Okta login pages instead of Jira data. Even though you're authenticated in your browser (`mwinit` is working), the MCP server runs as a separate process and doesn't have access to browser cookies.

### Root Cause
```
RBKS-MCP-Servers → Jira API → Okta Login Page (HTML)
```

The MCP server needs its own authentication configuration.

### Evidence
```bash
# When calling jira_search_issues:
Result: <!DOCTYPE html>...Ring - Sign In...Okta...
```

## ✅ What's Working

1. **mwinit authentication**: You're authenticated with Amazon's Midway
2. **MCP client code**: Fixed and working (can communicate with MCP server)
3. **Jira Max MVP agent**: Code is ready and tested with mock data
4. **Test scripts**: All infrastructure in place

## 🚀 Path Forward: Use Atlassian MCP Instead

### Why Atlassian MCP?
- **Simple authentication**: Just needs Jira URL + email + API token
- **No Okta complexity**: Direct API token authentication
- **Better features**: Native support for sprints, worklogs, links
- **Already tested**: We know it works with `uvx`

### What You Need (5 minutes)

1. **Get Jira API Token**
   - Go to: https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Name it: "Jira Max MCP"
   - Copy the token

2. **Provide 3 Things**
   - Jira URL: `https://jira.atl.ring.com`
   - Your email: (the one you use for Jira)
   - API token: (from step 1)

3. **I'll Configure It**
   - Update `.kiro/settings/mcp.json`
   - Test the connection
   - Update Jira Max agent to use Atlassian MCP

## 📋 Alternative: Fix RBKS MCP Authentication

If you prefer to use RBKS MCP, we need to:

1. Find how RBKS MCP expects Jira credentials
2. Configure environment variables or config file
3. Restart the MCP server

**Problem**: RBKS MCP documentation doesn't clearly explain Jira authentication setup.

## 🎯 Recommendation

**Use Atlassian MCP** - it's faster, simpler, and better documented.

Once you provide the 3 pieces of info above, we'll have real Jira data working in ~5 minutes.

## 📝 Files Ready

- `test_flan_jira.py` - Test script (ready to use with Atlassian MCP)
- `tpm-slack-bot/src/agents/jira_max/jira_max_agent.py` - MVP agent
- `tpm-slack-bot/src/services/mcp_client.py` - Fixed MCP client
- `ATLASSIAN_MCP_SETUP_INSTRUCTIONS.md` - Setup guide

## ⏱️ Time Estimate

- **With Atlassian MCP**: 5 minutes (once you provide credentials)
- **With RBKS MCP**: Unknown (need to research authentication)

---

**Next Step**: Provide Jira URL, email, and API token for Atlassian MCP setup.
