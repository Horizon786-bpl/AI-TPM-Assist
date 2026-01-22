#!/usr/bin/env python3
"""
Simple Interactive Jira Max Agent
Works directly with Kiro MCP tools (no subprocess)
"""

import sys
import os

# Add tpm-slack-bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot'))

from src.agents.jira_max_mvp import JiraMaxMVP


class SimpleMCPClient:
    """Simple MCP client that uses Kiro's tools directly"""
    
    def call_tool(self, tool_name, arguments):
        """Call MCP tool through Kiro"""
        # This will be called from within Kiro context
        # where mcp_rbks_mcp_servers_* functions are available
        if tool_name == "jira_search_issues":
            return mcp_rbks_mcp_servers_jira_search_issues(**arguments)
        elif tool_name == "jira_get_issue":
            return mcp_rbks_mcp_servers_jira_get_issue(**arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")


def main():
    """Run interactive Jira Max agent"""
    
    print("\n" + "=" * 80)
    print("  🤖 JIRA MAX - Your Intelligent Jira Assistant")
    print("=" * 80)
    print("\n  I can help you analyze your Jira projects!")
    print()
    
    # Initialize
    mcp = SimpleMCPClient()
    jira_max = JiraMaxMVP(mcp)
    
    # Ask for project
    print("📋 Which Jira project would you like to analyze?")
    print()
    print("Examples: PODFLAN, RCIT, or any other project key")
    print()
    
    project = input("Enter project key: ").strip().upper()
    
    if not project:
        print("No project entered. Exiting.")
        return 1
    
    print(f"\n✅ Analyzing project: {project}\n")
    
    # Show menu
    while True:
        print("\n" + "=" * 80)
        print(f"📊 What would you like to know about {project}?")
        print("=" * 80)
        print()
        print("  1. 👥 Team Workload")
        print("  2. 🐛 Quality Metrics")
        print("  3. 🔍 Search Issues")
        print("  4. 🚀 Releasable Items")
        print("  5. 📈 Full Report")
        print("  6. ❌ Quit")
        print()
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            print("\n" + "=" * 80)
            print(f"👥 Team Workload for {project}")
            print("=" * 80 + "\n")
            
            result = jira_max.team_workload(project)
            print(result["report"])
            
            print(f"\n📊 Team size: {result['team_size']} | Active issues: {result['total_issues']}")
            
        elif choice == "2":
            print("\n" + "=" * 80)
            print(f"🐛 Quality Metrics for {project}")
            print("=" * 80 + "\n")
            
            result = jira_max.features_vs_bugs(project, days=60)
            print(result["report"])
            
            print(f"\n📊 Bug ratio: {result['bug_ratio']:.1f}% | Total: {result['total']}")
            
        elif choice == "3":
            print("\n🔍 Search Issues")
            query = input("Enter search term: ").strip()
            if query:
                result = jira_max.search_issues(query, project, max_results=5)
                print("\n" + result["report"])
            
        elif choice == "4":
            print("\n" + "=" * 80)
            print(f"🚀 Releasable Items in {project}")
            print("=" * 80 + "\n")
            
            result = jira_max.search_issues(
                f'project = {project} AND status = Releasable',
                project,
                max_results=10
            )
            print(result["report"])
            
            if result['total'] > 0:
                print(f"\n🎉 {result['total']} issues ready to deploy!")
            
        elif choice == "5":
            print("\n" + "=" * 80)
            print(f"📈 Full Report for {project}")
            print("=" * 80 + "\n")
            
            # Team workload
            print("1/3 - Team Workload")
            print("-" * 80)
            result = jira_max.team_workload(project)
            print(result["report"])
            
            # Quality
            print("\n2/3 - Quality Metrics")
            print("-" * 80)
            result = jira_max.features_vs_bugs(project, days=60)
            print(result["report"])
            
            # Releasable
            print("\n3/3 - Releasable Items")
            print("-" * 80)
            result = jira_max.search_issues(
                f'project = {project} AND status = Releasable',
                project,
                max_results=5
            )
            if result['total'] > 0:
                print(f"🚀 {result['total']} issues ready to deploy")
                for item in result['results']:
                    print(f"  • {item['key']}: {item['summary'][:60]}...")
            else:
                print("📋 No releasable items")
            
            print("\n✅ Report complete!")
            
        elif choice == "6":
            print("\n👋 Goodbye!\n")
            return 0
        else:
            print("\n⚠️  Invalid choice\n")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    sys.exit(main())
