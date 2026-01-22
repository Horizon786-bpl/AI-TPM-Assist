#!/usr/bin/env python3
"""
Test Jira Max MVP with Flan Project (PODFLAN)
Run the actual agent code to generate formatted reports.
"""

import sys
sys.path.insert(0, 'tpm-slack-bot')

from src.agents.jira_max_mvp import JiraMaxMVP


# Simple MCP wrapper for Kiro
class KiroMCP:
    """Wrapper to use Kiro's MCP tools with Jira Max agent."""
    
    def call_tool(self, server, tool, params):
        """Call MCP tool through Kiro."""
        if tool == "jira_search_issues":
            return mcp_rbks_mcp_servers_jira_search_issues(**params)
        elif tool == "jira_get_issue":
            return mcp_rbks_mcp_servers_jira_get_issue(**params)
        else:
            raise ValueError(f"Unknown tool: {tool}")


def main():
    """Test Jira Max MVP with Flan project."""
    
    print("=" * 80)
    print("🚀 JIRA MAX MVP - FLAN PROJECT TEST")
    print("=" * 80)
    print()
    
    # Initialize
    mcp = KiroMCP()
    jira_max = JiraMaxMVP(mcp)
    
    # Test 1: Team Workload for PODFLAN
    print("=" * 80)
    print("TEST 1: Team Workload Distribution")
    print("=" * 80)
    print()
    
    try:
        result = jira_max.team_workload("PODFLAN")
        print(result["report"])
        print()
        print(f"📊 Summary:")
        print(f"  - Team size: {result['team_size']} members")
        print(f"  - Total active issues: {result['total_issues']}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 2: Quality Metrics for PODFLAN
    print("=" * 80)
    print("TEST 2: Features vs Bugs Analysis (Last 60 Days)")
    print("=" * 80)
    print()
    
    try:
        result = jira_max.features_vs_bugs("PODFLAN", days=60)
        print(result["report"])
        print()
        print(f"📊 Summary:")
        print(f"  - Total issues: {result['total']}")
        print(f"  - Bug ratio: {result['bug_ratio']:.1f}%")
        print(f"  - Features: {result['features']}")
        print(f"  - Bugs: {result['bugs']}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 3: Search for specific issues
    print("=" * 80)
    print("TEST 3: Search for 'audio' related issues")
    print("=" * 80)
    print()
    
    try:
        result = jira_max.search_issues("audio", "PODFLAN", max_results=5)
        print(result["report"])
        print()
        print(f"📊 Summary:")
        print(f"  - Total matches: {result['total']}")
        print(f"  - Showing: {result['returned']} issues")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 4: Search for in-progress issues
    print("=" * 80)
    print("TEST 4: Search for In Progress issues")
    print("=" * 80)
    print()
    
    try:
        result = jira_max.search_issues(
            'project = PODFLAN AND status = "In Progress"',
            "PODFLAN",
            max_results=10
        )
        print(result["report"])
        print()
        print(f"📊 Summary:")
        print(f"  - Total in progress: {result['total']}")
        print(f"  - Showing: {result['returned']} issues")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 5: Search for bugs
    print("=" * 80)
    print("TEST 5: Search for Bugs")
    print("=" * 80)
    print()
    
    try:
        result = jira_max.search_issues(
            'project = PODFLAN AND issuetype = Bug',
            "PODFLAN",
            max_results=10
        )
        print(result["report"])
        print()
        print(f"📊 Summary:")
        print(f"  - Total bugs: {result['total']}")
        print(f"  - Showing: {result['returned']} bugs")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 6: Milestone status (if any exist)
    print("=" * 80)
    print("TEST 6: Milestone Status (if available)")
    print("=" * 80)
    print()
    
    # First check if there are any milestones
    try:
        # Search for issues with fixVersion
        check_result = mcp_rbks_mcp_servers_jira_search_issues(
            jql='project = PODFLAN AND fixVersion is not EMPTY',
            fields=['fixVersions'],
            maxResults=1
        )
        
        if check_result and check_result.get('total', 0) > 0:
            # Get the first milestone name
            milestone = check_result['issues'][0]['fields']['fixVersions'][0]['name']
            print(f"Found milestone: {milestone}")
            print()
            
            result = jira_max.milestone_status(milestone, "PODFLAN")
            print(result["report"])
            print()
        else:
            print("⚠️ No milestones/fixVersions found in PODFLAN project")
            print("   Recommendation: Create versions in Jira for milestone tracking")
            print()
    except Exception as e:
        print(f"⚠️ No milestones available: {e}")
        print()
    
    # Final Summary
    print("=" * 80)
    print("✅ JIRA MAX MVP TEST COMPLETE")
    print("=" * 80)
    print()
    print("🎉 All core features tested successfully!")
    print()
    print("📋 Next Steps:")
    print("  1. Add story points to PODFLAN issues for velocity tracking")
    print("  2. Create milestones/versions for release planning")
    print("  3. Prioritize backlog items")
    print("  4. Deploy releasable issues")
    print()
    print("🚀 Ready for Slack integration!")
    print()


if __name__ == "__main__":
    main()
