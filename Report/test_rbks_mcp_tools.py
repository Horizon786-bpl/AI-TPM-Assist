#!/usr/bin/env python3
"""
Test RBKS MCP Built-in Tools

Explore what tools are available in RBKS MCP
"""

import sys
import os

# Add tpm-slack-bot/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot', 'src'))

from services.mcp_client import MCPClient

def main():
    print("🔧 RBKS MCP Tools Explorer")
    print("=" * 70)
    
    # Initialize MCP client
    client = MCPClient("rbks-mcp-servers")
    
    print("\n📋 Available Tools:\n")
    
    # List all available tools
    tools = client.list_tools()
    
    # Group tools by category
    jira_tools = []
    confluence_tools = []
    slack_tools = []
    figma_tools = []
    bitbucket_tools = []
    other_tools = []
    
    for tool in tools:
        name = tool['name']
        if 'jira' in name.lower():
            jira_tools.append(tool)
        elif 'confluence' in name.lower():
            confluence_tools.append(tool)
        elif 'slack' in name.lower():
            slack_tools.append(tool)
        elif 'figma' in name.lower():
            figma_tools.append(tool)
        elif 'bitbucket' in name.lower():
            bitbucket_tools.append(tool)
        else:
            other_tools.append(tool)
    
    # Print by category
    if jira_tools:
        print(f"🎫 JIRA Tools ({len(jira_tools)}):")
        for tool in jira_tools[:5]:  # Show first 5
            print(f"  • {tool['name']}")
            if 'description' in tool:
                print(f"    {tool['description'][:80]}...")
        if len(jira_tools) > 5:
            print(f"  ... and {len(jira_tools) - 5} more")
        print()
    
    if confluence_tools:
        print(f"📄 Confluence Tools ({len(confluence_tools)}):")
        for tool in confluence_tools:
            print(f"  • {tool['name']}")
            if 'description' in tool:
                print(f"    {tool['description'][:80]}...")
        print()
    
    if slack_tools:
        print(f"💬 Slack Tools ({len(slack_tools)}):")
        for tool in slack_tools[:5]:
            print(f"  • {tool['name']}")
            if 'description' in tool:
                print(f"    {tool['description'][:80]}...")
        if len(slack_tools) > 5:
            print(f"  ... and {len(slack_tools) - 5} more")
        print()
    
    if figma_tools:
        print(f"🎨 Figma Tools ({len(figma_tools)}):")
        for tool in figma_tools[:3]:
            print(f"  • {tool['name']}")
        if len(figma_tools) > 3:
            print(f"  ... and {len(figma_tools) - 3} more")
        print()
    
    if bitbucket_tools:
        print(f"🔀 Bitbucket Tools ({len(bitbucket_tools)}):")
        for tool in bitbucket_tools[:3]:
            print(f"  • {tool['name']}")
        if len(bitbucket_tools) > 3:
            print(f"  ... and {len(bitbucket_tools) - 3} more")
        print()
    
    if other_tools:
        print(f"🔧 Other Tools ({len(other_tools)}):")
        for tool in other_tools[:3]:
            print(f"  • {tool['name']}")
        if len(other_tools) > 3:
            print(f"  ... and {len(other_tools) - 3} more")
        print()
    
    print("=" * 70)
    print(f"\n✅ Total: {len(tools)} tools available")
    
    # Test a simple Jira search
    print("\n🧪 Testing Jira Search...")
    try:
        result = client.call_tool(
            "jira_search_issues",
            {
                "jql": "project = RCIT AND status = Open",
                "maxResults": 3
            }
        )
        
        if isinstance(result, dict) and 'issues' in result:
            print(f"✅ Found {len(result['issues'])} issues")
            for issue in result['issues'][:2]:
                print(f"  • {issue['key']}: {issue['fields']['summary'][:60]}...")
        else:
            print(f"⚠️  Unexpected result: {type(result)}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
