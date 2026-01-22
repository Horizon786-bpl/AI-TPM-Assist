#!/usr/bin/env python3
"""Quick test to see if MCP connection works"""

import sys
import os

print("Testing MCP connection...")

try:
    from mcp import ClientSession, StdioServerParameters
    print("✅ MCP library imported")
except Exception as e:
    print(f"❌ Failed to import MCP: {e}")
    sys.exit(1)

try:
    import asyncio
    print("✅ asyncio imported")
except Exception as e:
    print(f"❌ Failed to import asyncio: {e}")
    sys.exit(1)

print("\n✅ Basic imports work!")
print("\nNow testing RBKS MCP server connection...")
print("This will try to connect to the MCP server...")

async def test_connection():
    try:
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@ring-mcp/server"],
            env=None
        )
        
        async with ClientSession(server_params.command, server_params.args) as session:
            await session.initialize()
            print("✅ Connected to RBKS MCP server!")
            
            # List available tools
            tools_result = await session.list_tools()
            print(f"✅ Found {len(tools_result.tools)} tools")
            print("\nFirst 5 tools:")
            for tool in tools_result.tools[:5]:
                print(f"  - {tool.name}")
            
            return True
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_connection())
    if result:
        print("\n✅ MCP is working!")
    else:
        print("\n❌ MCP connection failed")
        print("\nTroubleshooting:")
        print("1. Make sure Kiro is running")
        print("2. Check if RBKS MCP is configured in Kiro")
        print("3. Try: mwinit -o")
