#!/usr/bin/env python3
"""
Simple test of RBKS MCP jira_search_issues tool
"""

import sys
import os

# Add tpm-slack-bot/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot', 'src'))

from services.mcp_client import RBKSMCPClient

def main():
    print("🧪 Testing RBKS MCP jira_search_issues")
    print("=" * 70)
    
    # Initialize client
    client = RBKSMCPClient()
    
    # Test 1: Search for open RCIT issues
    print("\n📋 Test 1: Search open RCIT issues")
    print("-" * 70)
    
    try:
        result = client.search_jira_issues(
            jql="project = RCIT AND status = Open",
            max_results=5
        )
        
        print(f"✅ Success! Result type: {type(result)}")
        
        if isinstance(result, dict):
            if 'issues' in result:
                print(f"\n📊 Found {len(result['issues'])} issues:")
                for issue in result['issues']:
                    key = issue.get('key', 'N/A')
                    summary = issue.get('fields', {}).get('summary', 'N/A')
                    status = issue.get('fields', {}).get('status', {}).get('name', 'N/A')
                    print(f"  • {key}: {summary[:60]}...")
                    print(f"    Status: {status}")
            else:
                print(f"\n⚠️  No 'issues' key in result")
                print(f"Keys: {list(result.keys())}")
        else:
            print(f"\n⚠️  Result is not a dict: {result}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Search for Flan-related issues
    print("\n\n📋 Test 2: Search Flan-related issues")
    print("-" * 70)
    
    try:
        result = client.search_jira_issues(
            jql="text ~ 'Flan' AND status = Open",
            max_results=3
        )
        
        print(f"✅ Success! Found {len(result.get('issues', []))} issues")
        
        if isinstance(result, dict) and 'issues' in result:
            for issue in result['issues']:
                key = issue.get('key', 'N/A')
                summary = issue.get('fields', {}).get('summary', 'N/A')
                print(f"  • {key}: {summary[:60]}...")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Test complete!")

if __name__ == "__main__":
    main()
