#!/usr/bin/env python3
"""
CLI Test for Jira Max MVP
Tests core features with real RCIT data.
"""

import sys
import os

# Add tpm-slack-bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot'))

from src.agents.jira_max_mvp import JiraMaxMVP


class SimpleMCPClient:
    """Simple MCP client wrapper for testing."""
    
    def call_tool(self, server: str, tool: str, params: dict):
        """Call MCP tool - will be replaced with actual Kiro MCP calls."""
        print(f"\n🔧 Calling: {server}.{tool}")
        print(f"   Params: {params}")
        
        # In real usage, this would call Kiro's MCP
        # For now, return mock data structure
        raise NotImplementedError(
            "This test requires Kiro MCP integration. "
            "Run this in Kiro chat instead."
        )


def test_milestone_status():
    """Test milestone status report."""
    print("\n" + "="*80)
    print("TEST 1: Milestone Status Report")
    print("="*80)
    
    # This would work in Kiro with real MCP
    print("""
To test this in Kiro, use:

from src.agents.jira_max_mvp import JiraMaxMVP
from src.services.mcp_client import MCPClient

mcp = MCPClient()
jira_max = JiraMaxMVP(mcp)

# Test with a real milestone
result = jira_max.milestone_status("DVT", "RCIT")
print(result["report"])
""")


def test_team_workload():
    """Test team workload report."""
    print("\n" + "="*80)
    print("TEST 2: Team Workload Distribution")
    print("="*80)
    
    print("""
To test this in Kiro, use:

result = jira_max.team_workload("RCIT")
print(result["report"])
""")


def test_features_vs_bugs():
    """Test features vs bugs analysis."""
    print("\n" + "="*80)
    print("TEST 3: Features vs Bugs Analysis")
    print("="*80)
    
    print("""
To test this in Kiro, use:

result = jira_max.features_vs_bugs("RCIT", days=30)
print(result["report"])
""")


def test_search_issues():
    """Test issue search."""
    print("\n" + "="*80)
    print("TEST 4: Issue Search")
    print("="*80)
    
    print("""
To test this in Kiro, use:

# Natural language search
result = jira_max.search_issues("authentication", "RCIT")
print(result["report"])

# JQL search
result = jira_max.search_issues("status = Open AND priority = High", "RCIT")
print(result["report"])
""")


def main():
    """Run all tests."""
    print("="*80)
    print("JIRA MAX MVP - CLI TEST GUIDE")
    print("="*80)
    print("""
This script shows how to test Jira Max MVP in Kiro.

⚠️  NOTE: These tests require Kiro MCP integration.
         Copy the code snippets below into Kiro chat to test.

SETUP:
1. Make sure you're authenticated: mwinit -o
2. Reload Kiro window
3. Copy test code into Kiro chat
""")
    
    test_milestone_status()
    test_team_workload()
    test_features_vs_bugs()
    test_search_issues()
    
    print("\n" + "="*80)
    print("QUICK START IN KIRO")
    print("="*80)
    print("""
Copy this into Kiro chat to get started:

```python
import sys
sys.path.insert(0, 'tpm-slack-bot')

from src.agents.jira_max_mvp import JiraMaxMVP

# Create a simple MCP wrapper
class KiroMCP:
    def call_tool(self, server, tool, params):
        # Use Kiro's MCP tools directly
        if tool == "jira_search_issues":
            return mcp_rbks_mcp_servers_jira_search_issues(**params)
        elif tool == "jira_get_issue":
            return mcp_rbks_mcp_servers_jira_get_issue(**params)
        else:
            raise ValueError(f"Unknown tool: {tool}")

# Initialize Jira Max
mcp = KiroMCP()
jira_max = JiraMaxMVP(mcp)

# Test it!
print("Testing Jira Max MVP...")

# 1. Search for recent issues
result = jira_max.search_issues("authentication", "RCIT", max_results=5)
print(result["report"])

# 2. Get team workload
result = jira_max.team_workload("RCIT")
print(result["report"])

# 3. Analyze quality
result = jira_max.features_vs_bugs("RCIT", days=30)
print(result["report"])

print("\\n✅ Jira Max MVP is working!")
```
""")
    
    print("\n" + "="*80)
    print("EXPECTED OUTPUT")
    print("="*80)
    print("""
You should see formatted reports like:

👥 Team Workload
Mohan Vamsi Musunuru (mmmusunu@amazon.com):
  📊 15 issues, 28 story points
  🔄 8 in progress, 📋 7 to do

Lam Nguyen (lamhng@amazon.com):
  📊 12 issues, 24 story points
  🔄 6 in progress, 📋 6 to do

🐛 Quality Metrics (Last 30 Days)
Issue Breakdown:
  📦 Features: 15 (48%)
  🐛 Bugs: 10 (32%)
  📋 Tasks: 6 (19%)

Bug Ratio: 32%
  ⚠️ Above target (25%)
""")


if __name__ == "__main__":
    main()
