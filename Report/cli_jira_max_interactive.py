#!/usr/bin/env python3
"""
Interactive Jira Max Agent
Asks user for project and provides intelligent analysis
"""

import sys
import os

# Add tpm-slack-bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot'))

from src.agents.jira_max_mvp import JiraMaxMVP
from src.services.mcp_client import MCPClient


class JiraMaxInteractiveAgent:
    """Interactive Jira Max agent that converses with user"""
    
    def __init__(self):
        """Initialize the agent"""
        self.mcp = None
        self.jira_max = None
        self.project = None
        
    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "=" * 80)
        print("  🤖 JIRA MAX - Your Intelligent Jira Assistant")
        print("=" * 80)
        print("\n  I can help you analyze your Jira projects!")
        print("  I'll provide insights on:")
        print("    • Team workload distribution")
        print("    • Quality metrics (bugs vs features)")
        print("    • Issue search and filtering")
        print("    • Releasable items")
        print("    • And more!")
        print()
    
    def initialize(self):
        """Initialize MCP and Jira Max"""
        print("🔧 Initializing connection to Jira...")
        
        try:
            self.mcp = MCPClient("rbks-mcp-servers")
            self.jira_max = JiraMaxMVP(self.mcp)
            print("✅ Connected successfully!\n")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {e}\n")
            print("Make sure:")
            print("  1. You're authenticated with: mwinit -o")
            print("  2. RBKS MCP is configured in Kiro")
            print("  3. Kiro is running\n")
            return False
    
    def ask_project(self):
        """Ask user for project key"""
        print("=" * 80)
        print("📋 Which Jira project would you like to analyze?")
        print("=" * 80)
        print()
        print("Examples:")
        print("  • PODFLAN - Flan Chime Pro Audio-Visual Features")
        print("  • RCIT - Ring Continuous Improvement Team")
        print("  • Or any other project key")
        print()
        
        while True:
            project = input("Enter project key (or 'quit' to exit): ").strip().upper()
            
            if project.lower() == 'quit':
                return None
            
            if not project:
                print("⚠️  Please enter a project key\n")
                continue
            
            # Validate project exists
            print(f"\n🔍 Checking if project '{project}' exists...")
            try:
                result = self.mcp.call_tool("jira_search_issues", {
                    "jql": f"project = {project}",
                    "fields": ["key"],
                    "maxResults": 1
                })
                
                if result and result.get("total", 0) > 0:
                    total = result["total"]
                    print(f"✅ Found project '{project}' with {total} issues!\n")
                    return project
                else:
                    print(f"❌ Project '{project}' not found or has no issues")
                    print("   Please try another project key\n")
            except Exception as e:
                print(f"❌ Error checking project: {e}\n")
    
    def show_menu(self):
        """Show analysis options menu"""
        print("\n" + "=" * 80)
        print(f"📊 What would you like to know about {self.project}?")
        print("=" * 80)
        print()
        print("  1. 👥 Team Workload - Who's working on what?")
        print("  2. 🐛 Quality Metrics - How many bugs vs features?")
        print("  3. 🔍 Search Issues - Find specific issues")
        print("  4. 🚀 Releasable Items - What's ready to deploy?")
        print("  5. 📈 Full Report - Complete project analysis")
        print("  6. 🔄 Change Project - Analyze a different project")
        print("  7. ❌ Quit")
        print()
    
    def handle_team_workload(self):
        """Handle team workload analysis"""
        print("\n" + "=" * 80)
        print(f"👥 Analyzing Team Workload for {self.project}...")
        print("=" * 80 + "\n")
        
        try:
            result = self.jira_max.team_workload(self.project)
            print(result["report"])
            
            print("\n" + "-" * 80)
            print("📊 Summary:")
            print(f"  • Team size: {result['team_size']} members")
            print(f"  • Total active issues: {result['total_issues']}")
            if result['team_size'] > 0:
                avg = result['total_issues'] / result['team_size']
                print(f"  • Average load: {avg:.1f} issues per person")
                
                if avg > 5:
                    print("\n  ⚠️  High workload detected! Consider redistributing work.")
                elif avg < 2:
                    print("\n  ✅ Team has capacity for more work.")
                else:
                    print("\n  ✅ Workload looks balanced.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def handle_quality_metrics(self):
        """Handle quality metrics analysis"""
        print("\n" + "=" * 80)
        print(f"🐛 Analyzing Quality Metrics for {self.project}...")
        print("=" * 80 + "\n")
        
        # Ask for time period
        print("How far back should I look?")
        print("  1. Last 30 days")
        print("  2. Last 60 days")
        print("  3. Last 90 days")
        print("  4. Custom")
        
        choice = input("\nEnter choice (1-4, default: 2): ").strip() or "2"
        
        days_map = {"1": 30, "2": 60, "3": 90}
        days = days_map.get(choice, 60)
        
        if choice == "4":
            try:
                days = int(input("Enter number of days: ").strip())
            except:
                days = 60
        
        print(f"\n📅 Analyzing last {days} days...\n")
        
        try:
            result = self.jira_max.features_vs_bugs(self.project, days=days)
            print(result["report"])
            
            print("\n" + "-" * 80)
            print("📊 Summary:")
            print(f"  • Total issues: {result['total']}")
            print(f"  • Bug ratio: {result['bug_ratio']:.1f}%")
            print(f"  • Features: {result['features']}")
            print(f"  • Bugs: {result['bugs']}")
            print(f"  • Tasks: {result['tasks']}")
            
            if result['bug_ratio'] > 30:
                print("\n  🔴 High bug ratio! Quality needs attention.")
            elif result['bug_ratio'] > 25:
                print("\n  ⚠️  Bug ratio above 25% target.")
            else:
                print("\n  ✅ Bug ratio within target!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def handle_search(self):
        """Handle issue search"""
        print("\n" + "=" * 80)
        print(f"🔍 Search Issues in {self.project}")
        print("=" * 80 + "\n")
        
        print("What would you like to search for?")
        print("Examples:")
        print("  • 'audio' - Find audio-related issues")
        print("  • 'bug' - Find all bugs")
        print("  • 'status = \"In Progress\"' - JQL query")
        print()
        
        query = input("Enter search term or JQL: ").strip()
        
        if not query:
            print("⚠️  No search term entered")
            return
        
        max_results = input("\nHow many results? (default: 10): ").strip() or "10"
        try:
            max_results = int(max_results)
        except:
            max_results = 10
        
        print(f"\n🔍 Searching for '{query}'...\n")
        
        try:
            result = self.jira_max.search_issues(query, self.project, max_results=max_results)
            print(result["report"])
            
            print("\n" + "-" * 80)
            print(f"📊 Found {result['total']} matching issues (showing {result['returned']})")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def handle_releasable(self):
        """Handle releasable items check"""
        print("\n" + "=" * 80)
        print(f"🚀 Finding Releasable Items in {self.project}...")
        print("=" * 80 + "\n")
        
        try:
            result = self.jira_max.search_issues(
                f'project = {self.project} AND status = Releasable',
                self.project,
                max_results=20
            )
            print(result["report"])
            
            print("\n" + "-" * 80)
            if result['total'] > 0:
                print(f"🎉 {result['total']} issues are ready to deploy!")
                print("\n💡 Recommendation: Release these items to:")
                print("   • Reduce work in progress")
                print("   • Deliver value to customers")
                print("   • Unblock dependent work")
            else:
                print("📋 No releasable items found.")
                print("   All work is either in progress or already deployed.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def handle_full_report(self):
        """Generate full project report"""
        print("\n" + "=" * 80)
        print(f"📈 Generating Full Report for {self.project}...")
        print("=" * 80 + "\n")
        
        print("This will analyze:")
        print("  ✓ Team workload")
        print("  ✓ Quality metrics")
        print("  ✓ Releasable items")
        print("  ✓ Recent activity")
        print()
        
        confirm = input("Continue? (Y/n): ").strip().lower()
        if confirm and confirm != 'y':
            return
        
        # Team workload
        print("\n" + "=" * 80)
        print("1/4 - Team Workload")
        print("=" * 80)
        try:
            result = self.jira_max.team_workload(self.project)
            print(result["report"])
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Quality metrics
        print("\n" + "=" * 80)
        print("2/4 - Quality Metrics (Last 60 Days)")
        print("=" * 80)
        try:
            result = self.jira_max.features_vs_bugs(self.project, days=60)
            print(result["report"])
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Releasable items
        print("\n" + "=" * 80)
        print("3/4 - Releasable Items")
        print("=" * 80)
        try:
            result = self.jira_max.search_issues(
                f'project = {self.project} AND status = Releasable',
                self.project,
                max_results=10
            )
            if result['total'] > 0:
                print(f"\n🚀 {result['total']} issues ready to deploy!")
                for item in result['results'][:5]:
                    print(f"  • {item['key']}: {item['summary'][:60]}...")
            else:
                print("\n📋 No releasable items found")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # In progress
        print("\n" + "=" * 80)
        print("4/4 - In Progress Work")
        print("=" * 80)
        try:
            result = self.jira_max.search_issues(
                f'project = {self.project} AND status = "In Progress"',
                self.project,
                max_results=10
            )
            print(f"\n🔄 {result['total']} issues in progress")
            for item in result['results'][:5]:
                print(f"  • {item['key']}: {item['summary'][:60]}... ({item['assignee']})")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 80)
        print("✅ Full Report Complete!")
        print("=" * 80)
    
    def run(self):
        """Main agent loop"""
        self.print_banner()
        
        if not self.initialize():
            return 1
        
        # Ask for project
        self.project = self.ask_project()
        if not self.project:
            print("\n👋 Goodbye!\n")
            return 0
        
        # Main interaction loop
        while True:
            self.show_menu()
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == "1":
                self.handle_team_workload()
            elif choice == "2":
                self.handle_quality_metrics()
            elif choice == "3":
                self.handle_search()
            elif choice == "4":
                self.handle_releasable()
            elif choice == "5":
                self.handle_full_report()
            elif choice == "6":
                self.project = self.ask_project()
                if not self.project:
                    print("\n👋 Goodbye!\n")
                    return 0
            elif choice == "7":
                print("\n👋 Thanks for using Jira Max! Goodbye!\n")
                return 0
            else:
                print("\n⚠️  Invalid choice. Please enter 1-7.\n")
            
            input("\nPress Enter to continue...")


def main():
    """Entry point"""
    agent = JiraMaxInteractiveAgent()
    return agent.run()


if __name__ == "__main__":
    sys.exit(main())
