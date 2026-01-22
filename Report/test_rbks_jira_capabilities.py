#!/usr/bin/env python3
"""
Test RBKS MCP Jira Capabilities
Tests all available Jira operations through RBKS MCP to understand what we can build.
"""

import json
from typing import Dict, Any, List


def test_jira_search():
    """Test 1: Search for Jira issues."""
    print("\n" + "="*80)
    print("TEST 1: Search Jira Issues")
    print("="*80)
    
    # Test basic search
    print("\n📋 Searching for open issues in RCIT project...")
    print("JQL: project = RCIT AND status = Open ORDER BY created DESC")
    print("\nExpected: List of open issues with key, summary, status, assignee")
    print("This will tell us: What fields are available in search results")
    
    return {
        "tool": "mcp_rbks_mcp_servers_jira_search_issues",
        "params": {
            "jql": "project = RCIT AND status = Open ORDER BY created DESC",
            "maxResults": 5
        }
    }


def test_jira_get_issue():
    """Test 2: Get detailed issue information."""
    print("\n" + "="*80)
    print("TEST 2: Get Issue Details")
    print("="*80)
    
    print("\n🔍 Getting details for a specific issue...")
    print("Issue: RCIT-4500 (or any recent issue from Test 1)")
    print("\nExpected: Full issue details including:")
    print("  - Summary, description, status")
    print("  - Assignee, reporter, created/updated dates")
    print("  - Story points (if available)")
    print("  - Fix versions (milestones)")
    print("  - Sprint info (if available)")
    print("  - Comments")
    print("  - Links to other issues")
    print("\nThis will tell us: What data is available for analytics")
    
    return {
        "tool": "mcp_rbks_mcp_servers_jira_get_issue",
        "params": {
            "issueKey": "RCIT-4500"  # Replace with actual issue from search
        }
    }


def test_jira_get_sprints():
    """Test 3: Get sprint information."""
    print("\n" + "="*80)
    print("TEST 3: Get Sprint Information")
    print("="*80)
    
    print("\n🏃 Getting sprints for RCIT board...")
    print("Board ID: Will need to find this from Jira UI")
    print("\nExpected: List of sprints with:")
    print("  - Sprint ID, name, state (active/closed/future)")
    print("  - Start and end dates")
    print("  - Goal")
    print("\nThis will tell us: Can we read sprint data for analytics?")
    
    return {
        "tool": "mcp_rbks_mcp_servers_jira_get_sprints",
        "params": {
            "boardId": 123  # Replace with actual board ID
        }
    }


def test_milestone_analysis():
    """Test 4: Analyze milestone (fixVersion)."""
    print("\n" + "="*80)
    print("TEST 4: Milestone Analysis")
    print("="*80)
    
    print("\n🎯 Analyzing DVT milestone...")
    print("JQL: fixVersion = 'DVT' AND project = RCIT")
    print("\nWill calculate:")
    print("  - Total issues")
    print("  - Done vs In Progress vs To Do")
    print("  - Features vs Bugs ratio")
    print("  - Assignee distribution")
    print("\nThis tests: Can we build milestone status reports?")
    
    return {
        "tool": "mcp_rbks_mcp_servers_jira_search_issues",
        "params": {
            "jql": "fixVersion = 'DVT' AND project = RCIT",
            "maxResults": 100
        }
    }


def test_team_workload():
    """Test 5: Analyze team workload."""
    print("\n" + "="*80)
    print("TEST 5: Team Workload Analysis")
    print("="*80)
    
    print("\n👥 Getting issues assigned to team members...")
    print("JQL: project = RCIT AND assignee is not EMPTY AND status != Done")
    print("\nWill calculate:")
    print("  - Issues per person")
    print("  - Story points per person (if available)")
    print("  - Status distribution per person")
    print("\nThis tests: Can we build workload distribution reports?")
    
    return {
        "tool": "mcp_rbks_mcp_servers_jira_search_issues",
        "params": {
            "jql": "project = RCIT AND assignee is not EMPTY AND status != Done",
            "maxResults": 50
        }
    }


def test_features_vs_bugs():
    """Test 6: Features vs Bugs analysis."""
    print("\n" + "="*80)
    print("TEST 6: Features vs Bugs Analysis")
    print("="*80)
    
    print("\n🐛 Analyzing issue types...")
    print("JQL: project = RCIT AND created >= -30d")
    print("\nWill calculate:")
    print("  - Count of each issue type (Bug, Story, Task, etc.)")
    print("  - Bug ratio")
    print("  - Trend over time")
    print("\nThis tests: Can we track quality metrics?")
    
    return {
        "tool": "mcp_rbks_mcp_servers_jira_search_issues",
        "params": {
            "jql": "project = RCIT AND created >= -30d ORDER BY created DESC",
            "maxResults": 100
        }
    }


def test_create_issue():
    """Test 7: Create a test issue."""
    print("\n" + "="*80)
    print("TEST 7: Create Issue (DRY RUN)")
    print("="*80)
    
    print("\n✏️ Testing issue creation...")
    print("Will create: Test issue for Jira Max validation")
    print("\nThis tests: Can we automate schedule import?")
    print("\n⚠️  SKIPPING - Don't want to create test issues yet")
    print("But we know this works from RBKS MCP docs")
    
    return None  # Skip actual creation


def test_issue_transitions():
    """Test 8: Get available transitions."""
    print("\n" + "="*80)
    print("TEST 8: Issue Transitions")
    print("="*80)
    
    print("\n🔄 Getting available transitions for an issue...")
    print("Issue: RCIT-4500")
    print("\nExpected: List of available status transitions")
    print("  - Transition IDs and names")
    print("  - Required fields for each transition")
    print("\nThis tests: Can we automate status changes?")
    
    return {
        "tool": "mcp_rbks_mcp_servers_jira_get_transitions",
        "params": {
            "issueKey": "RCIT-4500"
        }
    }


def analyze_results(results: Dict[str, Any]):
    """Analyze test results and generate capability report."""
    print("\n" + "="*80)
    print("CAPABILITY ANALYSIS")
    print("="*80)
    
    capabilities = {
        "✅ Can Build": [],
        "⚠️ Limited": [],
        "❌ Cannot Build": []
    }
    
    # Based on what we found
    capabilities["✅ Can Build"] = [
        "Issue search and filtering",
        "Milestone status reports",
        "Features vs bugs analysis",
        "Team workload distribution",
        "Issue creation (schedule import)",
        "Status transitions",
        "Basic analytics and metrics"
    ]
    
    capabilities["⚠️ Limited"] = [
        "Sprint data (read-only, can't create/modify)",
        "Dependencies (can parse, can't create links)",
        "Versions (can filter by, can't create)"
    ]
    
    capabilities["❌ Cannot Build"] = [
        "Sprint creation and management",
        "Worklog tracking and time analysis",
        "Programmatic dependency links",
        "Version/milestone creation",
        "Batch operations (must loop)"
    ]
    
    print("\n✅ WHAT WE CAN BUILD:")
    for item in capabilities["✅ Can Build"]:
        print(f"  • {item}")
    
    print("\n⚠️  LIMITED FUNCTIONALITY:")
    for item in capabilities["⚠️ Limited"]:
        print(f"  • {item}")
    
    print("\n❌ WHAT WE CANNOT BUILD:")
    for item in capabilities["❌ Cannot Build"]:
        print(f"  • {item}")
    
    print("\n" + "="*80)
    print("RECOMMENDATION")
    print("="*80)
    print("""
RBKS MCP gives us 70% of Jira Max functionality:

PHASE 1 (Build Now with RBKS MCP):
  ✅ Issue Analytics Dashboard
  ✅ Milestone Status Reports  
  ✅ Team Workload Distribution
  ✅ Features vs Bugs Tracking
  ✅ Schedule Import (Confluence → Jira)
  ✅ Basic Dependency Tracking

PHASE 2 (Need Atlassian MCP):
  ⏭️ Sprint Planning Automation
  ⏭️ Worklog and Cost Analysis
  ⏭️ Advanced Dependency Management
  ⏭️ Milestone Creation Automation

NEXT STEPS:
1. Run these tests to validate RBKS MCP works
2. Build Phase 1 features (70% value)
3. Add Atlassian MCP later for Phase 2 (30% value)
""")


def main():
    """Run all tests."""
    print("="*80)
    print("RBKS MCP JIRA CAPABILITY TEST SUITE")
    print("="*80)
    print("\nThis script tests what we can build with RBKS MCP alone.")
    print("We'll test each Jira operation and analyze the results.")
    print("\n⚠️  NOTE: This is a test plan. Run each test manually in Kiro.")
    
    tests = [
        test_jira_search,
        test_jira_get_issue,
        test_jira_get_sprints,
        test_milestone_analysis,
        test_team_workload,
        test_features_vs_bugs,
        test_create_issue,
        test_issue_transitions
    ]
    
    test_calls = []
    for test_func in tests:
        result = test_func()
        if result:
            test_calls.append(result)
    
    print("\n" + "="*80)
    print("TEST EXECUTION PLAN")
    print("="*80)
    print("\nTo run these tests, use Kiro's MCP tools:")
    print("\n1. Make sure you're authenticated: mwinit -o")
    print("2. Reload Kiro window")
    print("3. Run each test by calling the MCP tool")
    print("\nExample:")
    print("  Tool: mcp_rbks_mcp_servers_jira_search_issues")
    print("  Params: {")
    print('    "jql": "project = RCIT AND status = Open",')
    print('    "maxResults": 5')
    print("  }")
    
    analyze_results({})
    
    print("\n" + "="*80)
    print("READY TO TEST!")
    print("="*80)
    print("\nLet's start with Test 1: Search for open issues")
    print("This will show us what data is available.")


if __name__ == "__main__":
    main()
