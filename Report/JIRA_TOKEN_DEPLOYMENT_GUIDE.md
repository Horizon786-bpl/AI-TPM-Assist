# Jira Token Deployment Guide - Local vs AWS

## The Question from IT

**IT is asking:** "Where will this run? What's your AWS account?"

**Your Answer Depends On:** Development phase vs Production deployment

## Deployment Phases

### Phase 1: MVP Development (NOW) - Local Machine ✅

**Where it runs:** Your local MacBook
**Authentication:** Your personal mwinit credentials
**Network:** Amazon corporate network (VPN)
**No IP whitelisting needed** - You're already authenticated via mwinit

**What to tell IT:**
```
Phase 1 (Current): Running locally on my MacBook for development and testing.
I'm using mwinit authentication, so no special network access needed.
This is for personal productivity and testing only.
```

**Why this works:**
- RBKS MCP uses your mwinit session
- You're on Amazon corporate network
- Jira recognizes your Amazon credentials
- No API token needed for local development with RBKS MCP

### Phase 2: Production Slack Bot - AWS Lambda 🚀

**Where it runs:** AWS Lambda in your team's AWS account
**Authentication:** Jira API token (stored in AWS Secrets Manager)
**Network:** AWS VPC with NAT Gateway
**IP whitelisting:** May be needed

**What to tell IT:**
```
Phase 2 (Future): Will deploy to AWS Lambda for production Slack bot.

AWS Account: [Your team's AWS account ID]
Region: us-west-2 (or your region)
Service: AWS Lambda
Network: Will use NAT Gateway with static IP

I'll provide the NAT Gateway IP address once infrastructure is set up.
For now, I just need the token for local development and testing.
```

## Recommended Approach

### Option A: Start Simple (Recommended) 👍

**Step 1: Local Development (No Token Needed)**
```bash
# Use RBKS MCP with mwinit
cd tpm-slack-bot
python cli_test_jira_max_standalone.py
```

**Step 2: Request Token for Future Use**
```
Subject: Jira API Token Request for Future AWS Deployment

I'm building a TPM automation tool that will eventually run in AWS Lambda.

Current Phase: Local development using mwinit (no token needed yet)
Future Phase: AWS Lambda deployment (will need API token)

Can I get a Jira API token now for testing, with the understanding that
I'll provide AWS infrastructure details (NAT Gateway IP) when we deploy
to production?

For now, the token will only be used from my local machine for testing.
```

**Step 3: Deploy to AWS Later**
- Set up AWS infrastructure
- Get NAT Gateway static IP
- Provide IP to IT for whitelisting
- Deploy Lambda with token from Secrets Manager

### Option B: Full Production Setup (Complex) 🏗️

If IT requires full details upfront:

**1. Set Up AWS Infrastructure First**
```bash
# Create VPC with NAT Gateway
# Get static Elastic IP
# Note the IP address
```

**2. Provide Complete Details to IT**
```
Deployment Architecture:

Local Development:
- Machine: MacBook Pro
- Network: Amazon Corporate VPN
- IP: Dynamic (corporate network)
- Use: Testing and development only

Production Deployment:
- Platform: AWS Lambda
- AWS Account: [Account ID]
- Region: us-west-2
- VPC: [VPC ID]
- NAT Gateway IP: [Static IP]
- Use: Production Slack bot for TPM team
```

## What You Actually Need

### For MVP Testing (Now)
**No API token needed!** 

Your current setup works because:
- ✅ RBKS MCP uses mwinit authentication
- ✅ You're on Amazon corporate network
- ✅ Jira recognizes your credentials
- ✅ No IP whitelisting required

### For Production Slack Bot (Later)
**API token required**

Because:
- ❌ AWS Lambda can't use mwinit
- ❌ Lambda needs API token authentication
- ❌ May need IP whitelisting for security

## Simplified IT Ticket

Here's what to actually tell IT:

```
Subject: Jira API Token Request for Automation Development

Hi IT Team,

I'm developing automation tools for TPM workflows and need a Jira API token.

Current Setup:
- Development: Local MacBook using mwinit (working now)
- Testing: Personal use for building automation tools

Future Plans:
- Will deploy to AWS Lambda for team Slack bot
- Will provide AWS infrastructure details when ready
- Will request IP whitelisting at that time

For now, I just need a token for local development and testing.

Required Permissions:
- Read access to Jira projects (PODFLAN, RCIT, PODHEXA)
- Search issues
- View issue details
- View project metadata

User: danissid@amazon.com
Jira Instance: jira.atl.ring.com

Thank you!
```

## Network Architecture

### Current (Local Development)
```
Your MacBook
    ↓ (mwinit auth)
Amazon Corporate Network
    ↓
jira.atl.ring.com
    ✅ Authenticated via mwinit
```

### Future (AWS Production)
```
Slack User
    ↓
Slack API
    ↓
AWS Lambda (us-west-2)
    ↓
NAT Gateway (Static IP: X.X.X.X)
    ↓
jira.atl.ring.com
    ✅ Authenticated via API token
    ✅ IP whitelisted
```

## AWS Account Information

If IT asks for AWS account details:

**For Development:**
```
Not applicable - running locally on corporate network
```

**For Production (when ready):**
```
AWS Account: [Get from your team's AWS admin]
Region: us-west-2
Service: Lambda
VPC: [Will be created]
NAT Gateway IP: [Will be provided after setup]
```

## Security Considerations

### Local Development
- ✅ Token stored in `~/.kiro/settings/mcp.json` (not in git)
- ✅ File permissions: `chmod 600 ~/.kiro/settings/mcp.json`
- ✅ Only accessible from your machine

### AWS Production
- ✅ Token stored in AWS Secrets Manager
- ✅ Lambda IAM role has read-only access to secret
- ✅ Token rotated every 90 days
- ✅ CloudWatch logs don't expose token
- ✅ VPC security groups restrict access

## Timeline

### Week 1-2: Local Development (NOW)
- ✅ Use RBKS MCP with mwinit
- ✅ Build and test Jira Max agent
- ✅ Test with real PODFLAN data
- ⏳ Request API token from IT

### Week 3-4: Token Testing
- 🔧 Receive API token from IT
- 🔧 Configure Atlassian MCP locally
- 🔧 Test both RBKS and Atlassian MCPs
- 🔧 Compare features and performance

### Week 5-8: AWS Deployment
- 🏗️ Set up AWS infrastructure
- 🏗️ Create VPC with NAT Gateway
- 🏗️ Get static IP address
- 🏗️ Request IP whitelisting from IT
- 🏗️ Deploy Lambda function
- 🏗️ Integrate with Slack

## What to Do Right Now

**1. Keep Using RBKS MCP (No Token Needed)**
```bash
cd tpm-slack-bot
python cli_test_jira_max_standalone.py
# Enter: PODFLAN
# Test your agent!
```

**2. File Simple IT Ticket**
- Request token for "local development and testing"
- Mention future AWS deployment
- Don't provide AWS details yet (you don't have them)

**3. When You Get Token**
- Test locally first
- Verify it works with Atlassian MCP
- Then plan AWS deployment

## Common IT Questions & Answers

**Q: What's your machine IP?**
A: "I'm on Amazon corporate network using mwinit authentication. For local development, I don't need IP whitelisting. For future AWS deployment, I'll provide the NAT Gateway IP."

**Q: What AWS account?**
A: "For now, this is local development only. When we deploy to AWS, I'll provide the account details and request IP whitelisting at that time."

**Q: Why do you need this?**
A: "Building automation tools for TPM workflows - project status reporting, risk analysis, and team workload tracking. Currently testing locally, will deploy to AWS Lambda for team use later."

**Q: Is this production?**
A: "Not yet - this is development and testing phase. Production deployment will come later with proper AWS infrastructure and security review."

## Bottom Line

**For IT Ticket:**
- ✅ Request token for "local development"
- ✅ Mention future AWS deployment
- ❌ Don't provide AWS account yet (you don't need it now)
- ❌ Don't provide IP address (not needed for local dev)

**For MVP Testing:**
- ✅ Keep using RBKS MCP (works now!)
- ✅ No token needed for current setup
- ✅ Test everything locally first

**For Production:**
- ⏳ Set up AWS infrastructure later
- ⏳ Get NAT Gateway IP
- ⏳ Provide to IT for whitelisting
- ⏳ Deploy with proper security
