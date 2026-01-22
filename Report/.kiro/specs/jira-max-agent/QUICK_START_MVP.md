# Jira Max MVP - Quick Start (2-3 Days)

## 🎯 Goal: Get Core Features Working FAST

Focus on the **highest value features** that TPMs need most:
1. Milestone status tracking
2. Features vs bugs analysis
3. Basic issue search

Skip for MVP:
- ❌ Sprint planning (complex)
- ❌ Schedule import (complex)
- ❌ Dependency management (requires Atlassian MCP)
- ❌ Worklog analysis (requires Atlassian MCP)

## 🚀 Day 1: Basic Structure (4 hours)

### Step 1: Create Agent Structure (30 min)

```bash
cd tpm-slack-bot/src/agents
mkdir jira_max
touch jira_max/__init__.py
touch jira_max/jira_max_agent.py
```

### Step 2: Implement Basic Agent (2 hours)

**File:** `src/agents/jira_max/jira_max_agent.py`

```python
"""Jira Max Agent - MVP Version"""
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class JiraMaxAgent:
    """Simplified Jira Max agent for MVP."""
    
    def __init__(self, rbks_client, bedrock_client):
        self.rbks = rbks_client
        self.bedrock = bedrock_client
    
    def execute(self, query: str, project_key: str = "RCIT") -> Dict[str, Any]:
        """Execute Jira Max query."""
        
        # Classify intent
        intent = self._classify_intent(query)
        
        if "milestone" in intent or "status" in intent:
            return self.get_milestone_status(project_key, query)
        elif "features" in intent or "bugs" in intent:
            return self.analyze_features_vs_bugs(project_key)
        elif "search" in intent or "find" in intent:
            return self.search_issues(query, project_key)
        else:
            return self.get_project_overview(project_key)
    
    def get_milestone_status(self, project_key: str, milestone_name: str = None) -> Dict:
        """Get milestone status - CORE FEATURE #1"""
        
        # Search for issues in milestone
        if milestone_name:
            jql = f'project = {project_key} AND fixVersion = "{milestone_name}"'
        else:
            jql = f'project = {project_key} AND fixVersion is not EMPTY'
        
        issues = self.rbks.search_issues(jql, max_results=500)
        
        # Calculate metrics
        total = len(issues)
        done = sum(1 for i in issues if i.get('status') == 'Done')
        in_progress = sum(1 for i in issues if i.get('status') == 'In Progress')
        todo = total - done - in_progress
        
        features = sum(1 for i in issues if i.get('type') in ['Story', 'Epic'])
        bugs = sum(1 for i in issues if i.get('type') == 'Bug')
        
        return {
            'milestone': milestone_name or 'All Milestones',
            'total_issues': total,
            'completed': done,
            'in_progress': in_progress,
            'todo': todo,
            'completion_pct': int(done / total * 100) if total > 0 else 0,
            'features': features,
            'bugs': bugs,
            'bug_ratio': int(bugs / total * 100) if total > 0 else 0
        }
    
    def analyze_features_vs_bugs(self, project_key: str) -> Dict:
        """Analyze features vs bugs - CORE FEATURE #2"""
        
        jql = f'project = {project_key} AND status != Done'
        issues = self.rbks.search_issues(jql, max_results=500)
        
        features = [i for i in issues if i.get('type') in ['Story', 'Epic']]
        bugs = [i for i in issues if i.get('type') == 'Bug']
        
        return {
            'total_open': len(issues),
            'features': len(features),
            'bugs': len(bugs),
            'bug_ratio': int(len(bugs) / len(issues) * 100) if issues else 0,
            'recommendation': self._get_bug_recommendation(len(bugs), len(issues))
        }
    
    def search_issues(self, query: str, project_key: str) -> Dict:
        """Search issues - CORE FEATURE #3"""
        
        jql = f'project = {project_key} AND text ~ "{query}"'
        issues = self.rbks.search_issues(jql, max_results=50)
        
        return {
            'query': query,
            'found': len(issues),
            'issues': [
                {
                    'key': i.get('key'),
                    'summary': i.get('summary'),
                    'status': i.get('status'),
                    'type': i.get('type')
                }
                for i in issues[:10]  # Top 10
            ]
        }
    
    def get_project_overview(self, project_key: str) -> Dict:
        """Get project overview - BONUS FEATURE"""
        
        jql = f'project = {project_key}'
        all_issues = self.rbks.search_issues(jql, max_results=1000)
        
        open_issues = [i for i in all_issues if i.get('status') != 'Done']
        closed_issues = [i for i in all_issues if i.get('status') == 'Done']
        
        return {
            'project': project_key,
            'total_issues': len(all_issues),
            'open': len(open_issues),
            'closed': len(closed_issues),
            'completion_pct': int(len(closed_issues) / len(all_issues) * 100) if all_issues else 0
        }
    
    def _classify_intent(self, query: str) -> str:
        """Simple intent classification."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['milestone', 'status', 'progress']):
            return 'milestone'
        elif any(word in query_lower for word in ['features', 'bugs', 'ratio']):
            return 'features_bugs'
        elif any(word in query_lower for word in ['search', 'find']):
            return 'search'
        else:
            return 'overview'
    
    def _get_bug_recommendation(self, bugs: int, total: int) -> str:
        """Get recommendation based on bug ratio."""
        if total == 0:
            return "No issues found"
        
        ratio = bugs / total * 100
        
        if ratio > 30:
            return "⚠️ High bug ratio! Consider a bug bash."
        elif ratio > 20:
            return "⚡ Moderate bug ratio. Monitor closely."
        else:
            return "✅ Healthy bug ratio."
    
    def format_for_slack(self, result: Dict) -> str:
        """Format result for Slack."""
        
        if 'milestone' in result:
            return self._format_milestone_status(result)
        elif 'bug_ratio' in result and 'features' in result:
            return self._format_features_bugs(result)
        elif 'issues' in result:
            return self._format_search_results(result)
        else:
            return self._format_overview(result)
    
    def _format_milestone_status(self, data: Dict) -> str:
        """Format milestone status for Slack."""
        return f"""
📊 *Milestone Status: {data['milestone']}*

*Progress:*
✅ Completed: {data['completed']} ({data['completion_pct']}%)
🔄 In Progress: {data['in_progress']}
📋 To Do: {data['todo']}
━━━━━━━━━━━━━━━━
📦 Total: {data['total_issues']} issues

*Breakdown:*
🎯 Features: {data['features']}
🐛 Bugs: {data['bugs']} ({data['bug_ratio']}%)
"""
    
    def _format_features_bugs(self, data: Dict) -> str:
        """Format features vs bugs for Slack."""
        return f"""
📊 *Features vs Bugs Analysis*

*Open Issues:* {data['total_open']}
🎯 Features: {data['features']}
🐛 Bugs: {data['bugs']} ({data['bug_ratio']}%)

{data['recommendation']}
"""
    
    def _format_search_results(self, data: Dict) -> str:
        """Format search results for Slack."""
        results = f"🔍 *Search Results for: {data['query']}*\n\n"
        results += f"Found {data['found']} issues (showing top 10):\n\n"
        
        for issue in data['issues']:
            results += f"• *{issue['key']}* - {issue['summary']}\n"
            results += f"  Status: {issue['status']} | Type: {issue['type']}\n\n"
        
        return results
    
    def _format_overview(self, data: Dict) -> str:
        """Format project overview for Slack."""
        return f"""
📊 *Project Overview: {data['project']}*

*Total Issues:* {data['total_issues']}
📂 Open: {data['open']}
✅ Closed: {data['closed']}
📈 Completion: {data['completion_pct']}%
"""
```

### Step 3: Create CLI Test (1 hour)

**File:** `cli_test_jira_max_mvp.py`

```python
"""Quick CLI test for Jira Max MVP"""
import sys
sys.path.append('tpm-slack-bot')

from src.services.rbks_client import RBKSClient
from src.services.bedrock_client import BedrockClient
from src.agents.jira_max.jira_max_agent import JiraMaxAgent

def main():
    print("🚀 Jira Max MVP Test\n")
    
    # Initialize clients
    rbks = RBKSClient()
    bedrock = BedrockClient()
    agent = JiraMaxAgent(rbks, bedrock)
    
    # Test 1: Milestone Status
    print("=" * 50)
    print("TEST 1: Milestone Status")
    print("=" * 50)
    result = agent.execute("Show me DVT milestone status", "RCIT")
    print(agent.format_for_slack(result))
    
    # Test 2: Features vs Bugs
    print("\n" + "=" * 50)
    print("TEST 2: Features vs Bugs")
    print("=" * 50)
    result = agent.execute("Analyze features vs bugs", "RCIT")
    print(agent.format_for_slack(result))
    
    # Test 3: Search
    print("\n" + "=" * 50)
    print("TEST 3: Search Issues")
    print("=" * 50)
    result = agent.execute("Search for authentication issues", "RCIT")
    print(agent.format_for_slack(result))
    
    # Test 4: Overview
    print("\n" + "=" * 50)
    print("TEST 4: Project Overview")
    print("=" * 50)
    result = agent.execute("Show project overview", "RCIT")
    print(agent.format_for_slack(result))
    
    print("\n✅ All tests complete!")

if __name__ == "__main__":
    main()
```

### Step 4: Test It (30 min)

```bash
cd tpm-slack-bot
python ../cli_test_jira_max_mvp.py
```

**Expected Output:** Milestone status, features vs bugs, search results, project overview

---

## 🚀 Day 2: LangGraph Integration (3 hours)

### Step 1: Add to Workflow (1 hour)

Update `src/services/program_status_bot.py`:

```python
from src.agents.jira_max.jira_max_agent import JiraMaxAgent

# In __init__:
self.jira_max_agent = JiraMaxAgent(self.rbks_client, self.bedrock_client)

# Add node:
def jira_max_node(state: TPMState) -> TPMState:
    """Jira Max agent node."""
    query = state['user_query']
    result = self.jira_max_agent.execute(query)
    formatted = self.jira_max_agent.format_for_slack(result)
    
    state['agent_results']['jira_max'] = formatted
    return state

# Add to graph:
workflow.add_node("jira_max", jira_max_node)

# Add routing:
def route_query(state: TPMState) -> str:
    query = state['user_query'].lower()
    
    if any(word in query for word in ['milestone', 'jira', 'issues', 'bugs']):
        return "jira_max"
    # ... existing routing
```

### Step 2: Test Integration (1 hour)

```python
# cli_test_jira_max_integrated.py
from src.services.program_status_bot import ProgramStatusBot

bot = ProgramStatusBot()

# Test queries
queries = [
    "Show me DVT milestone status",
    "How many bugs do we have?",
    "Search for login issues"
]

for query in queries:
    print(f"\nQuery: {query}")
    result = bot.process_query(query)
    print(result)
```

### Step 3: Add Help Command (30 min)

```python
def get_help_text() -> str:
    return """
🤖 *Jira Max Commands*

*Milestone Status:*
• "Show DVT milestone status"
• "What's the progress on PVT?"

*Features vs Bugs:*
• "Analyze features vs bugs"
• "How many bugs do we have?"

*Search:*
• "Search for authentication issues"
• "Find issues about login"

*Overview:*
• "Show project overview"
• "Give me RCIT summary"
"""
```

---

## 🚀 Day 3: Slack Integration (2 hours)

### Step 1: Add Slack Handler (1 hour)

Update `src/handlers/slack_handler.py`:

```python
@app.command("/jira-max")
def handle_jira_max(ack, command, say):
    """Handle /jira-max command."""
    ack()
    
    query = command['text']
    
    if not query or query == "help":
        say(get_help_text())
        return
    
    # Show thinking message
    say("🔍 Analyzing Jira data...")
    
    # Process query
    bot = ProgramStatusBot()
    result = bot.process_query(query)
    
    # Send result
    say(result)
```

### Step 2: Test in Slack (30 min)

```bash
# Start Slack bot
cd tpm-slack-bot
python src/app.py
```

Test commands in Slack:
- `/jira-max Show DVT milestone status`
- `/jira-max Analyze features vs bugs`
- `/jira-max help`

### Step 3: Document (30 min)

Create quick user guide showing the 3 core commands.

---

## ✅ MVP Complete!

**What You Have:**
- ✅ Milestone status tracking
- ✅ Features vs bugs analysis
- ✅ Issue search
- ✅ Project overview
- ✅ LangGraph integration
- ✅ Slack integration
- ✅ CLI testing

**What You Can Do:**
- Track milestone progress
- Monitor bug ratios
- Search for issues
- Get project summaries

**Time Investment:** 2-3 days vs 10 weeks

---

## 🚀 Next Steps (When You Have Time)

### Week 2: Add Sprint Planning
- Use RBKS MCP to get sprint info
- Basic sprint status

### Week 3: Add Atlassian MCP
- Install Atlassian MCP
- Add worklog analysis
- Add dependency tracking

### Week 4: Advanced Features
- Schedule import
- AI-powered insights
- Custom reports

---

## 🎯 Success Criteria for MVP

- [ ] Can query milestone status in <5 seconds
- [ ] Can see features vs bugs ratio
- [ ] Can search issues by keyword
- [ ] Works via CLI
- [ ] Works via Slack
- [ ] No crashes on bad input

**Ship it and iterate!** 🚀
