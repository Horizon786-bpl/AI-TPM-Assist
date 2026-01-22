# RBKS MCP Server - Setup Complete! ✅

## What You Just Installed

**RBKS-MCP-Servers v1.5.1** - Ring's official MCP server with:
- ✅ Jira integration (search, get issues)
- ✅ Confluence integration (get pages, search)
- ✅ Slack integration
- ✅ Figma integration
- ✅ BitBucket integration
- ✅ Built-in Midway authentication
- ✅ No AWS costs!
- ✅ No Bedrock setup needed!

## How to Use in Kiro

### 1. Reload Kiro

Press `Cmd+Shift+P` → Type "Reload Window" → Press Enter

### 2. Use in Chat

Once reloaded, you can use these commands directly in Kiro chat:

**Confluence Examples:**
```
Get this Confluence page: https://confluence.atl.ring.com/spaces/RCPM/pages/2814198025/Flan

Search Confluence for "Flan project status"

What's on the Flan Confluence page?
```

**Jira Examples:**
```
Get Jira issue RING-1234

Search Jira for open bugs in Ring project

What's the status of RING-5678?
```

**Combined:**
```
Find all Jira issues related to Flan and summarize the Confluence page
```

## Available MCP Tools

The RBKS MCP server provides these tools (auto-approved in your config):

### Jira Tools
- `jira_search_issues` - Search for Jira issues with JQL
- `jira_get_issue` - Get details of a specific issue
- `jira_create_issue` - Create new issues
- `jira_update_issue` - Update existing issues
- `jira_add_comment` - Add comments to issues
- `jira_transition_issue` - Change issue status
- `jira_get_transitions` - Get available transitions
- `jira_get_sprints` - Get sprint information

### Confluence Tools
- `confluence_get_page` - Get page content (markdown format)
- `confluence_search_pages` - Search for pages
- `confluence_create_page` - Create new pages
- `confluence_update_page` - Update existing pages
- `confluence_get_spaces` - List available spaces
- `confluence_get_comment` - Get specific comments

### Slack Tools
- `slack_messages` - Get messages from channels
- `slack_search` - Search Slack
- `slack_get_threads` - Get thread replies
- `slack_post_message` - Post messages

### Figma Tools
- `figma_get_current_user` - Get user info
- `figma_get_file` - Get Figma file details
- `figma_get_team_projects` - List team projects
- And more...

### BitBucket Tools
- `bitbucket_list_projects` - List projects
- `bitbucket_get_repository` - Get repo details
- `bitbucket_list_pull_requests` - List PRs
- `bitbucket_get_file_content` - Get file content
- And more...

## Authentication

**Already done!** You authenticated with:
```bash
mwinit -o
```

**When to re-authenticate:**
- If you see authentication errors
- After your Midway session expires (usually 12 hours)
- Just run `mwinit -o` again

## Advantages Over Custom Solution

| Feature | Custom MCP | RBKS MCP |
|---------|------------|----------|
| Setup Time | Hours | ✅ 5 minutes |
| Authentication | Browser automation | ✅ Built-in Midway |
| Maintenance | You | ✅ Ring team |
| Features | Basic | ✅ Full API access |
| Cost | AWS Bedrock charges | ✅ Free |
| Updates | Manual | ✅ Automatic |
| Support | None | ✅ Ring team support |
| Team Sharing | Complex | ✅ Easy |

## Support

**Need help?**
- Slack: [#support-build-ai](https://ring.enterprise.slack.com/archives/C090LP0CUHF)
- Slack: [#rbks-build-ai-accelerate](https://ring.enterprise.slack.com/archives/C08UHJQAH7A)
- Wiki: https://w.amazon.com/bin/view/Ring/Teams/REx/PlatformEng/RBKS-MCP-Servers/

## What's Next?

1. **Reload Kiro** (Cmd+Shift+P → Reload Window)
2. **Try it out** - Ask Kiro to get a Confluence page or Jira issue
3. **Explore** - Try different combinations of Jira, Confluence, and Slack queries
4. **Share** - Tell your Ring teammates about this!

## Example Workflows

### Status Report
```
Get all open Jira issues assigned to me and summarize the Flan Confluence page
```

### Bug Investigation
```
Search Jira for bugs related to authentication and get the details of the top 3 issues
```

### Documentation Review
```
Search Confluence for API documentation and list all pages in the Engineering space
```

### Team Coordination
```
Get the latest messages from #flan-team Slack channel and check if there are any related Jira issues
```

## Troubleshooting

**"Authentication failed"**
- Run: `mwinit -o`
- Reload Kiro

**"MCP server not found"**
- Check: `toolbox list` (should show RBKS-MCP-Servers)
- Reload Kiro

**"Tool not available"**
- Check `.kiro/settings/mcp.json` is correct
- Reload Kiro

## Success! 🎉

You now have Ring's official MCP server set up and ready to use. No AWS costs, no Bedrock setup, no browser automation - just clean, authenticated access to all your Ring tools!

Enjoy! 🚀
