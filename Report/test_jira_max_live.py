#!/usr/bin/env python3
"""
Live test of Jira Max MVP using Kiro MCP tools.
Run this in Kiro to test with real RCIT data.
"""

import sys
sys.path.insert(0, 'tpm-slack-bot')

from src.agents.jira_max_mvp import JiraMaxMVP


def test_with_real_data():
    """Test Jira Max with real RCIT data using Kiro MCP."""
    
    print("="*80)
    print("JIRA MAX MVP - LIVE TEST")
    print("="*80)
    
    # Note: This will be run in Kiro where MCP tools are available
    print("\n⚠️  This test requires Kiro MCP tools.")
    print("Copy this entire file content into Kiro chat to run.\n")
    
    # Create MCP wrapper that uses Kiro's MCP tools
    class KiroMCP:
        """Wrapper for Kiro MCP tools."""
        
        def call_tool(self, server, tool, params):
            """Call MCP tool using Kiro's built-in functions."""
            if tool == "jira_search_issues":
                # In Kiro, this would call: mcp_rbks_mcp_servers_jira_search_issues
                print(f"   📞 Calling {tool} with {params.get('maxResults', 'all')} results")
                # Return mock structure for now
                return {
                    "issues": [],
                    "total": 0
                }
            else:
                raise ValueError(f"Unknown tool: {tool}")
    
    # Initialize Jira Max
    mcp = KiroMCP()
    jira_max = JiraMaxMVP(mcp)
    
    print("✅ Jira Max MVP initialized\n")
    
    # Test 1: Search for recent issues
    print("-" * 80)
    print("TEST 1: Search for 'grafana' issues")
    print("-" * 80)
    try:
        result = jira_max.search_issues("grafana", "RCIT", max_results=3)
        print(result.get("report", "No report generated"))
    except Exception as e:
        print(f"⚠️  Test requires live MCP: {e}")
    
    # Test 2: Team workload
    print("\n" + "-" * 80)
    print("TEST 2: Team Workload Distribution")
    print("-" * 80)
    try:
        result = jira_max.team_workload("RCIT")
        print(result.get("report", "No report generated"))
    except Exception as e:
        print(f"⚠️  Test requires live MCP: {e}")
    
    # Test 3: Quality metrics
    print("\n" + "-" * 80)
    print("TEST 3: Features vs Bugs (Last 30 Days)")
    print("-" * 80)
    try:
        result = jira_max.features_vs_bugs("RCIT", days=30)
        print(result.get("report", "No report generated"))
    except Exception as e:
        print(f"⚠️  Test requires live MCP: {e}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    print("\n💡 To run with real data, use this in Kiro chat:")
    print("""
# Replace KiroMCP.call_tool with actual MCP calls:
class KiroMCP:
    def call_tool(self, server, tool, params):
        if tool == "jira_search_issues":
            return mcp_rbks_mcp_servers_jira_search_issues(**params)
        elif tool == "jira_get_issue":
            return mcp_rbks_mcp_servers_jira_get_issue(**params)
        else:
            raise ValueError(f"Unknown tool: {tool}")
""")


if __name__ == "__main__":
    test_with_real_data()
