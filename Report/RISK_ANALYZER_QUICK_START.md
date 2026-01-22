# Risk Analyzer - Quick Start Guide

## TL;DR

The Risk Analyzer now reads **real Confluence data** instead of mock data.

## Test It Now

```bash
# Test with Flan
python3 tpm-slack-bot/cli_test_risk_real.py Flan

# Test with Hexa
python3 tpm-slack-bot/cli_test_risk_real.py Hexa

# Test with any program
python3 tpm-slack-bot/cli_test_risk_real.py [YourProgram]
```

## What You'll See

```
======================================================================
🔍 Risk Analyzer - REAL CONFLUENCE DATA TEST
======================================================================

Testing with: Flan

Initializing clients...
✅ Clients initialized

Creating Risk Analyzer Agent...
✅ Agent created

Analyzing risks for Flan...
----------------------------------------------------------------------

======================================================================
📄 Page: Flan
🔗 URL: https://confluence.atl.ring.com/spaces/RCPM/pages/2814198025/Flan
🏢 Brand: Ring
🚦 Status: GREEN
======================================================================

## 📋 Executive Summary
**Top 3 Risks:** Resource constraints, feature delivery delays, firmware compatibility issues
**Key Mitigation:** Phased delivery approach with daily cross-team scrums
**Action Required:** Immediate resource reallocation and timeline adjustment

---

## 🔴 Critical Risks (High Impact, Immediate Action Needed)
1. Resource Constraints
   - Impact: Potential 2-week timeline compression for Alpha Phase 2
   - Mitigation: Revised resource commitment, phased delivery approach
   - Owner: PM Device, PM App

[... more risks ...]

======================================================================
✅ SUCCESS - This is REAL data from Confluence!
======================================================================
```

## Key Points

1. **Real Data:** Fetches latest content from actual Confluence pages
2. **MCP Connection:** Uses RBKS MCP server to connect to Confluence
3. **AI Analysis:** Bedrock analyzes the content and generates risk report
4. **Production Ready:** Works in Slack bot and CLI

## Files

- **Agent:** `tpm-slack-bot/src/agents/risk_analyzer.py`
- **Test (Real):** `tpm-slack-bot/cli_test_risk_real.py` ← Use this!
- **Test (Mock):** `tpm-slack-bot/test_risk_analyzer.py` ← Old, uses fake data
- **Slack Bot:** `tpm-slack-bot/demo_bot.py`

## Difference from Before

**Before:**
- Used mock data (never changed)
- Fast but not real
- Good for testing logic only

**After:**
- Uses real Confluence data (always current)
- Slower but accurate
- Production-ready

## Use in Slack

```
@bot analyze risks for Flan
```

The Slack bot already uses real MCP connection!

---

**Status:** ✅ WORKING
**Date:** January 21, 2026
