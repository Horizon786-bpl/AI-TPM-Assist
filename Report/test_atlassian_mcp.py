#!/usr/bin/env python3
"""
Test script to check if Atlassian MCP server can work with Ring's Confluence.
This will help us understand the authentication flow.
"""

import subprocess
import json
import sys

def test_mcp_connection():
    """Test if we can connect to Atlassian MCP server."""
    
    print("=" * 80)
    print("TESTING ATLASSIAN MCP SERVER WITH RING CONFLUENCE")
    print("=" * 80)
    print()
    
    print("🔍 Step 1: Starting Atlassian MCP server...")
    print("   This will likely open a browser for OAuth authentication")
    print()
    
    # Try to run the MCP server
    try:
        result = subprocess.run(
            ["npx", "-y", "@atlassian/mcp-server-atlassian@latest"],
            env={
                "ATLASSIAN_INSTANCE_URL": "https://confluence.atl.ring.com"
            },
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print("STDOUT:")
        print(result.stdout)
        print()
        print("STDERR:")
        print(result.stderr)
        print()
        
        if result.returncode == 0:
            print("✓ MCP server started successfully!")
        else:
            print(f"⚠️  MCP server exited with code: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("⏳ MCP server is running (timeout after 10s - this is expected)")
        print("   The server is waiting for authentication...")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print()
    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print()
    print("1. The MCP server needs OAuth authentication")
    print("2. Check if a browser window opened for login")
    print("3. If it asks for Atlassian Cloud login, Ring's Confluence might not support it")
    print("4. Ring uses Midway SSO, which may not be compatible with standard OAuth")
    print()
    print("ALTERNATIVE APPROACH:")
    print("- Keep using browser automation (your current script)")
    print("- It already works with Midway authentication")
    print("- Can access both Confluence and Jira through browser")
    print()
    
    return True

if __name__ == "__main__":
    test_mcp_connection()
