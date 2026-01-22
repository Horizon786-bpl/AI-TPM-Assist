#!/usr/bin/env python3
"""Test Confluence search using Kiro MCP tools directly"""

import subprocess
import json

print("Testing Confluence search via Kiro MCP...")

# Use Kiro's MCP tool directly
try:
    # This calls the MCP tool through Kiro
    result = subprocess.run(
        ["npx", "-y", "@ring-mcp/server"],
        input='{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n',
        capture_output=True,
        text=True,
        timeout=10
    )
    
    print("STDOUT:", result.stdout[:500])
    print("STDERR:", result.stderr[:500])
    print("Return code:", result.returncode)
    
except subprocess.TimeoutExpired:
    print("❌ Command timed out")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*70)
print("The issue: RBKS MCP server needs to run as a persistent process")
print("It can't be called as a one-shot command")
print("\nSolution: Use the agents that were working before")
print("="*70)
