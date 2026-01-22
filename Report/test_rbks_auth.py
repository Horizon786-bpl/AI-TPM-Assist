#!/usr/bin/env python3
"""
Simple test to check if RBKS MCP authentication is working
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot/src'))

from services.real_confluence_client import RealRBKSClient

print("🔍 Testing RBKS MCP Authentication\n")
print("="*70)

try:
    print("1. Creating RBKS client...")
    rbks = RealRBKSClient()
    print("   ✅ Client created")
    
    print("\n2. Testing simple Confluence search...")
    results = rbks.search_confluence_pages(
        query='text ~ "Hexa"',
        limit=1
    )
    
    print(f"   ✅ Search successful! Found {len(results)} results")
    
    if results:
        print(f"\n   First result:")
        print(f"   - Title: {results[0]['title']}")
        print(f"   - ID: {results[0]['id']}")
        print(f"   - URL: {results[0]['url']}")
    
    print("\n" + "="*70)
    print("✅ AUTHENTICATION WORKING!")
    print("="*70)
    
except Exception as e:
    print(f"\n   ❌ Search failed: {e}")
    print("\n" + "="*70)
    print("❌ AUTHENTICATION FAILED!")
    print("="*70)
    print("\nPossible causes:")
    print("1. mwinit session expired - run: mwinit -o")
    print("2. RBKS MCP can't access terminal credentials")
    print("3. Okta authentication required")
    print("\nTo fix:")
    print("1. Run: mwinit -o")
    print("2. Wait for authentication to complete")
    print("3. Run this test again")

print()
