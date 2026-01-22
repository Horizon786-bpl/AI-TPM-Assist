"""Test Jira access via Kiro's MCP tools"""

# This script will be run by Kiro, which has direct access to MCP tools
# We'll use this to test if RBKS MCP Jira tools work

def test_jira_search():
    """Test searching Jira issues"""
    print("🔍 Testing Jira Search via RBKS MCP\n")
    
    # This will be executed by Kiro using its MCP tools
    # Kiro should call: mcp_rbks_mcp_servers_jira_search_issues
    
    print("Query: project = FLAN AND status != Done")
    print("\nKiro, please call the RBKS MCP tool:")
    print("  Tool: mcp_rbks_mcp_servers_jira_search_issues")
    print("  Args: {")
    print('    "jql": "project = FLAN AND status != Done",')
    print('    "maxResults": 10')
    print("  }")
    print("\nPlease show me the results!")

if __name__ == "__main__":
    test_jira_search()
