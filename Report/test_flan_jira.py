"""Quick test to get Flan open Jira issues using RBKS MCP"""
import sys
sys.path.append('tpm-slack-bot')

from src.services.mcp_client import MCPClient

def main():
    print("🔍 Fetching Flan Open Jira Issues...\n")
    
    try:
        mcp = MCPClient()
        
        # Search for open Flan issues
        print("Searching Jira with: project = FLAN AND status != Done\n")
        
        result = mcp.call_tool(
            "jira_search_issues",
            {
                "jql": "project = FLAN AND status != Done",
                "maxResults": 50
            }
        )
        
        # Debug: print raw result
        print(f"DEBUG: Result type: {type(result)}")
        print(f"DEBUG: Result: {result[:500] if isinstance(result, str) else result}\n")
        
        # Parse result if it's a string
        if isinstance(result, str):
            import json
            result = json.loads(result)
        
        # Handle different result formats
        if isinstance(result, dict):
            if 'issues' in result:
                issues = result['issues']
            elif 'results' in result:
                issues = result['results']
            else:
                issues = [result]
        elif isinstance(result, list):
            issues = result
        else:
            issues = []
        
        print(f"✅ Found {len(issues)} open issues\n")
        print("=" * 80)
        
        # Group by status
        by_status = {}
        for issue in issues:
            status = issue.get('status', 'Unknown') if isinstance(issue, dict) else 'Unknown'
            if status not in by_status:
                by_status[status] = []
            by_status[status].append(issue)
        
        # Print summary
        print("\n📊 FLAN OPEN ISSUES SUMMARY\n")
        for status, issues in sorted(by_status.items()):
            print(f"{status}: {len(issues)} issues")
        
        print("\n" + "=" * 80)
        print("\n📋 ISSUE DETAILS\n")
        
        # Print each issue
        for issue in issues[:20]:  # Show first 20
            if isinstance(issue, dict):
                print(f"🎫 {issue.get('key', 'N/A')} - {issue.get('summary', 'N/A')}")
                print(f"   Status: {issue.get('status', 'N/A')} | Type: {issue.get('type', 'N/A')} | Priority: {issue.get('priority', 'N/A')}")
                if issue.get('assignee'):
                    print(f"   Assignee: {issue['assignee']}")
            else:
                print(f"🎫 {issue}")
            print()
        
        if len(issues) > 20:
            print(f"... and {len(issues) - 20} more issues\n")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
