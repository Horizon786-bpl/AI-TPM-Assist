# TPM Slack Bot - Project Summary

## What We Built

A Slack bot that helps TPMs automate workflows, starting with Confluence page summarization.

## Project Status

✅ **Phase 1 Complete**: MVP Structure Ready
- Clean project setup with git
- Slack integration framework
- Mock clients for development
- Ready for local testing

## Architecture

```
User in Slack
    ↓
TPM Slack Bot (Python + Slack Bolt)
    ↓
├── RBKS MCP Client → Confluence/Jira data
└── AWS Bedrock Client → AI summaries (Claude)
```

## What's Implemented

### ✅ Core Framework
- Slack Bolt integration
- Socket Mode for real-time messaging
- Command parsing and routing
- Error handling
- Logging

### ✅ Confluence Summarizer (MVP)
- `@tpm-bot summarize <url>` command
- URL parsing and page ID extraction
- Mock RBKS MCP client (returns fake data)
- Mock Bedrock client (returns fake summaries)
- Slack Block Kit formatting

### ✅ Help System
- `@tpm-bot help` - Show commands
- `@tpm-bot about` - Bot information
- App mention handling

### ✅ Development Setup
- Virtual environment
- Requirements.txt
- .env configuration
- .gitignore
- Git repository initialized
- Comprehensive documentation

## File Structure

```
tpm-slack-bot/
├── README.md              # Project overview
├── SETUP.md               # Detailed setup guide
├── QUICKSTART.md          # 5-minute quick start
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
└── src/
    ├── bot.py            # Main bot entry point
    ├── handlers/
    │   ├── confluence.py # Confluence commands
    │   └── help.py       # Help commands
    └── services/
        ├── rbks_client.py    # RBKS MCP wrapper
        └── bedrock_client.py # AWS Bedrock wrapper
```

## Next Steps

### Immediate (This Week)
1. **Test locally with mock data**
   - Run bot
   - Test commands in Slack
   - Verify message formatting

2. **Get AWS Bedrock access**
   - Request Claude Sonnet 4.5 access
   - Test real AI summaries

3. **Integrate real RBKS MCP**
   - Replace mock client with real MCP calls
   - Test with actual Confluence pages

### Short Term (Next 2 Weeks)
4. **Deploy to AWS Lambda**
   - Package for Lambda
   - Set up API Gateway
   - Configure IAM roles
   - Test production deployment

5. **Add features**
   - Compare command (detect changes)
   - Multiple project tracking
   - Scheduled summaries

### Medium Term (Month 1-2)
6. **Jira integration**
   - Issue search
   - Issue summaries
   - Link Confluence + Jira

7. **Status monitoring**
   - Automatic status checks
   - Alert on changes
   - Daily reports

8. **Advanced features**
   - Meeting prep
   - Risk detection
   - Trend analysis

## How to Use (Current State)

### 1. Set Up
```bash
cd tpm-slack-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with Slack tokens
```

### 2. Run
```bash
python src/bot.py
```

### 3. Test in Slack
```
@tpm-bot help
@tpm-bot summarize https://confluence.atl.ring.com/spaces/RCPM/pages/2814198025/Flan
```

## Current Limitations

⚠️ **Using Mock Clients**
- Returns fake Confluence data
- Returns fake AI summaries
- Good for testing UI/UX
- Need real integrations for production

⚠️ **Local Only**
- Runs on your laptop
- Stops when you close terminal
- Need deployment for 24/7 operation

⚠️ **Limited Features**
- Only Confluence summarization
- No Jira integration yet
- No status monitoring yet
- No scheduled reports yet

## Success Criteria

### MVP Success (Week 1)
- ✅ Bot responds in Slack
- ✅ Parses Confluence URLs
- 🔄 Returns real summaries (need Bedrock)
- 🔄 Works with real Confluence pages (need RBKS MCP)

### Production Success (Month 1)
- Deployed to AWS Lambda
- Used by 5+ TPMs
- Summarizes 50+ pages/week
- 90%+ user satisfaction

### Scale Success (Month 3)
- All TPM team using it
- Jira integration working
- Automatic monitoring active
- Saves 2+ hours/week per TPM

## Technical Decisions

### Why Slack Bot?
- ✅ No UI to build
- ✅ Everyone uses Slack
- ✅ Easy to share
- ✅ Mobile ready
- ✅ Natural interface

### Why Mock Clients First?
- ✅ Test without AWS/MCP blockers
- ✅ Validate UX early
- ✅ Easy to swap for real clients
- ✅ Faster iteration

### Why AWS Bedrock?
- ✅ Latest Claude models
- ✅ Amazon-approved
- ✅ Good pricing
- ✅ Easy integration

### Why RBKS MCP?
- ✅ Ring's official tool
- ✅ Handles Midway auth
- ✅ Maintained by Ring team
- ✅ Full API access

## Git Repository

```bash
# Current state
git log --oneline
# b79d3eb feat: Initial TPM Slack Bot setup with Confluence summarizer

# To push to remote (when ready)
git remote add origin <your-git-url>
git push -u origin main
```

## Resources

- **Slack Bolt**: https://slack.dev/bolt-python/
- **RBKS MCP**: https://w.amazon.com/bin/view/Ring/Teams/REx/PlatformEng/RBKS-MCP-Servers/
- **AWS Bedrock**: https://aws.amazon.com/bedrock/
- **Owner**: danissid@amazon.com

## Questions to Answer

1. **Where to host?**
   - AWS Lambda (recommended)
   - EC2 instance
   - ECS container

2. **How to handle auth?**
   - Bot uses service account?
   - Bot uses user's Midway creds?
   - Hybrid approach?

3. **Data storage?**
   - DynamoDB for history?
   - S3 for snapshots?
   - No storage (stateless)?

4. **Monitoring?**
   - CloudWatch logs?
   - Custom dashboard?
   - Slack alerts?

## Success! 🎉

You now have:
- ✅ Clean project structure
- ✅ Git repository initialized
- ✅ Slack bot framework ready
- ✅ Mock clients for testing
- ✅ Comprehensive documentation
- ✅ Ready to test locally

Next: Test the bot, get AWS access, integrate real clients, deploy!
