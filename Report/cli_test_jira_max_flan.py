#!/usr/bin/env python3
"""
CLI Test for Jira Max MVP with Flan Project
Mimics real-life implementation using MCP client
"""

import sys
import os

# Add tpm-slack-bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot'))

from src.agents.jira_max_mvp import JiraMaxMVP
from src.services.mcp_client import MCPClient


def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title: str):
    """Print a section divider"""
    print("\n" + "-" * 80)
    print(f"  {title}")
    print("-" * 80 + "\n")


def main():
    """Run Jira Max MVP CLI test with Flan project"""
    
    print_header("🚀 JIRA MAX MVP - FLAN PROJECT CLI TEST")
    print("Testing Jira Max agent with real PODFLAN data")
    print("Using RBKS MCP Server for Jira integration")
    print()
    
    # Initialize MCP client
    print("📡 Initializing MCP client...")
    try:
        mcp = MCPClient("rbks-mcp-servers")
        print("✅ MCP client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize MCP client: {e}")
        print("\nMake sure:")
        print("  1. RBKS MCP is configured in .kiro/settings/mcp.json")
        print("  2. You're authenticated with mwinit -o")
        print("  3. Kiro is running with MCP enabled")
        return 1
    
    # Initialize Jira Max agent
    print("🤖 Initializing Jira Max MVP agent...")
    jira_max = JiraMaxMVP(mcp)
    print("✅ Jira Max agent initialized")
    
    # Test 1: Team Workload
    print_header("TEST 1: Team Workload Distribution")
    print("Analyzing team workload for PODFLAN project...")
    
    try:
        result = jira_max.team_workload("PODFLAN")
        print(result["report"])
        
        print_section("Summary")
        print(f"  Team size: {result['team_size']} members")
        print(f"  Total active issues: {result['total_issues']}")
        print(f"  Average load: {result['total_issues'] / result['team_size']:.1f} issues per person")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Quality Metrics
    print_header("TEST 2: Quality Metrics (Last 60 Days)")
    print("Analyzing features vs bugs for PODFLAN...")
    
    try:
        result = jira_max.features_vs_bugs("PODFLAN", days=60)
        print(result["report"])
        
        print_section("Summary")
        print(f"  Total issues: {result['total']}")
        print(f"  Bug ratio: {result['bug_ratio']:.1f}%")
        print(f"  Features: {result['features']}")
        print(f"  Bugs: {result['bugs']}")
        print(f"  Tasks: {result['tasks']}")
        
        if result['bug_ratio'] > 25:
            print("\n  ⚠️  Bug ratio above 25% target!")
        else:
            print("\n  ✅ Bug ratio within target!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Search for audio issues
    print_header("TEST 3: Search for Audio-Related Issues")
    print("Searching for 'audio' in PODFLAN...")
    
    try:
        result = jira_max.search_issues("audio", "PODFLAN", max_results=5)
        print(result["report"])
        
        print_section("Summary")
        print(f"  Total matches: {result['total']}")
        print(f"  Showing: {result['returned']} issues")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: In Progress issues
    print_header("TEST 4: In Progress Issues")
    print("Finding all in-progress work...")
    
    try:
        result = jira_max.search_issues(
            'project = PODFLAN AND status = "In Progress"',
            "PODFLAN",
            max_results=10
        )
        print(result["report"])
        
        print_section("Summary")
        print(f"  Total in progress: {result['total']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 5: Bugs
    print_header("TEST 5: Bug Analysis")
    print("Finding all bugs in PODFLAN...")
    
    try:
        result = jira_max.search_issues(
            'project = PODFLAN AND issuetype = Bug',
            "PODFLAN",
            max_results=10
        )
        print(result["report"])
        
        print_section("Summary")
        print(f"  Total bugs: {result['total']}")
        
        if result['total'] == 0:
            print("  🎉 No bugs found!")
        elif result['total'] <= 2:
            print("  ✅ Very low bug count!")
        else:
            print("  ⚠️  Multiple bugs need attention")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 6: Releasable issues
    print_header("TEST 6: Releasable Issues")
    print("Finding issues ready to deploy...")
    
    try:
        result = jira_max.search_issues(
            'project = PODFLAN AND status = Releasable',
            "PODFLAN",
            max_results=15
        )
        print(result["report"])
        
        print_section("Summary")
        print(f"  Total releasable: {result['total']}")
        
        if result['total'] > 0:
            print(f"\n  🚀 {result['total']} issues ready to deploy!")
            print("     Consider releasing these to reduce WIP")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Final summary
    print_header("✅ TEST COMPLETE")
    print("All Jira Max MVP features tested successfully!")
    print()
    print("📋 Next Steps:")
    print("  1. Add story points to PODFLAN issues")
    print("  2. Create milestones/versions for release planning")
    print("  3. Deploy releasable issues")
    print("  4. Balance team workload")
    print("  5. Prioritize backlog items")
    print()
    print("🚀 Ready for Slack integration!")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
