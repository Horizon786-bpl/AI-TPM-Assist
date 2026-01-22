#!/usr/bin/env python3
"""
Simple MCP Test - Test RBKS MCP connection directly
"""

import sys
import os

# Add tpm-slack-bot/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot', 'src'))

from services.mcp_client import RBKSMCPClient

print("="*70)
print("Testing RBKS MCP Connection")
print("="*70)
print()

try:
    print("🔧 Initializing RBKS MCP Client...")
    client = RBKSMCPClient()
    print("✅ Client initialized")
    print()
    
    print("🔍 Testing Confluence search...")
    print("   Query: 'type = page AND title ~ \"Flan\"'")
    print()
    
    results = client.search_confluence_pages(
        query='type = page AND title ~ "Flan"',
        limit=3
    )
    
    print(f"✅ Search completed! Found {len(results)} results")
    print()
    
    if results:
        print("📄 Results:")
        for i, page in enumerate(results, 1):
            print(f"   {i}. {page['title']}")
            print(f"      ID: {page['id']}")
            print(f"      URL: {page['url']}")
            print()
    else:
        print("⚠️  No results found")
        print()
    
    print("="*70)
    print("✅ MCP Test PASSED!")
    print("="*70)
    
except Exception as e:
    print()
    print("="*70)
    print("❌ MCP Test FAILED!")
    print("="*70)
    print()
    print(f"Error: {e}")
    print()
    
    import traceback
    print("Full traceback:")
    traceback.print_exc()
    print()
    
    sys.exit(1)
