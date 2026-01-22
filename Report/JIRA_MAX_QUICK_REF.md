# Jira Max - Quick Reference Card

## 🚀 Run It Now

```bash
python cli_test_jira_max_mvp.py
```

## 💬 Example Queries

### Milestone Status
```
"Show me DVT milestone status"
"What's the progress on PVT?"
"Give me MP status"
```

### Features vs Bugs
```
"Analyze features vs bugs"
"How many bugs do we have?"
"Show me bug ratio"
```

### Search
```
"Search for authentication issues"
"Find login problems"
"Look for API issues"
```

### Overview
```
"Show project overview"
"Give me RCIT summary"
"Project status"
```

## 📁 Files

- **Agent:** `tpm-slack-bot/src/agents/jira_max/jira_max_agent.py`
- **Test:** `cli_test_jira_max_mvp.py`
- **Guide:** `.kiro/specs/jira-max-agent/QUICK_START_MVP.md`
- **Docs:** `JIRA_MAX_MVP_READY.md`

## ⚡ Quick Customization

### Change Project Key
```python
# In cli_test_jira_max_mvp.py, line 20:
result = agent.execute("query", "YOUR_PROJECT_KEY")
```

### Add New Milestone
```python
# In jira_max_agent.py, _extract_milestone():
milestones = ['DVT', 'PVT', 'MP', 'YOUR_MILESTONE']
```

### Adjust Bug Threshold
```python
# In jira_max_agent.py, _get_bug_recommendation():
if ratio > 30:  # Change this number
    return "⚠️ High bug ratio!"
```

## 🎯 What Works

✅ Milestone tracking  
✅ Features vs bugs  
✅ Issue search  
✅ Project overview  
✅ Slack formatting  
✅ Error handling  

## 🔜 What's Next

⏭️ LangGraph integration  
⏭️ Slack bot integration  
⏭️ Sprint planning  
⏭️ Worklog analysis  

## 📊 Output Format

All results are formatted for Slack with:
- Emojis for visual clarity
- Progress bars
- Percentage calculations
- Recommendations

## 🐛 Common Issues

**"No issues found"**
→ Check project key and milestone name

**"Error initializing"**
→ Verify RBKS MCP is configured

**"Search returns nothing"**
→ Try broader search terms

## 💡 Pro Tips

1. Test with CLI first
2. Use real project keys
3. Start with milestone status
4. Iterate based on feedback
5. Add features gradually

## ⏱️ Time Investment

- **Setup:** 0 minutes (already done!)
- **First test:** 2 minutes
- **Customization:** 5-10 minutes
- **Integration:** 15-30 minutes

## 🎉 Success!

You now have a working Jira Max agent that can:
- Track milestones in seconds
- Analyze bug ratios
- Search issues instantly
- Provide project summaries

**Ship it and iterate!** 🚀
