# TPM Assistant - Multi-Agent System

A multi-agent system to automate Technical Program Manager (TPM) workflows at Ring.

## Vision

Build specialized AI agents that work together to handle common TPM tasks:
- Monitor project status across Confluence/Jira
- Track risks and issues
- Prepare for meetings
- Generate reports
- Communicate updates

## Architecture

```
Orchestrator Bot (coordinates all bots)
├── Status Monitor Bot (tracks project health)
├── Risk Bot (identifies and tracks risks)
├── Issue Tracker Bot (monitors Jira issues)
├── Meeting Prep Bot (prepares meeting materials)
└── Communication Bot (posts updates to Slack)
```

## Current Status

**Phase 1: Status Monitor Bot** (In Progress)
- ✅ RBKS MCP integration working
- 🚧 Building Status Monitor Bot
- ⏳ Other bots pending

## Technology Stack

- **MCP Integration**: RBKS-MCP-Servers (Jira, Confluence, Slack, etc.)
- **Language**: Python 3.11+
- **AI**: AWS Bedrock Claude (when available) or local LLM
- **Architecture**: Multi-agent with message passing

## Getting Started

See individual bot READMEs:
- [Status Monitor Bot](./bots/status-monitor/README.md)

## Development Approach

Building one bot at a time:
1. ✅ Validate RBKS MCP access
2. 🚧 Build Status Monitor Bot (MVP)
3. ⏳ Add Risk Bot
4. ⏳ Add Issue Tracker Bot
5. ⏳ Add Meeting Prep Bot
6. ⏳ Add Communication Bot
7. ⏳ Build Orchestrator

## Project Structure

```
tpm-assistant/
├── bots/
│   ├── status-monitor/    # Bot #1: Status monitoring
│   ├── risk/              # Bot #2: Risk tracking
│   ├── issue-tracker/     # Bot #3: Issue monitoring
│   ├── meeting-prep/      # Bot #4: Meeting preparation
│   └── communication/     # Bot #5: Slack updates
├── shared/
│   ├── mcp_client.py      # RBKS MCP client wrapper
│   ├── message_bus.py     # Inter-bot communication
│   └── utils.py           # Shared utilities
├── orchestrator/          # Coordinates all bots
└── tests/                 # Integration tests
```

## Authentication

Uses existing Midway authentication via RBKS MCP:
```bash
mwinit -o
```

## License

Internal Ring/Amazon use only.
