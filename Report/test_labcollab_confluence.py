#!/usr/bin/env python3
"""
Test LabCollab Confluence Search via RBKS MCP
"""

import sys
import os

# Add tpm-slack-bot/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot', 'src'))

from services.mcp_client import RBKSMCPClient

def main():
    print("🧪 Testing LabCollab Confluence Search")
    print("=" * 70)
    
    # Initialize client
    client = RBKSMCPClient()
    
    # Test 1: Search for "Flan" in LabCollab
    print("\n📋 Test 1: Search LabCollab for 'Flan'")
    print("-" * 70)
    
    try:
        result = client.mcp.call_tool(
            "lab_collab_confluence_search_pages",
            {
                "query": "text ~ 'Flan'",
                "limit": 5
            }
        )
        
        print(f"✅ Success! Result type: {type(result)}")
        
        if isinstance(result, dict):
            if 'results' in result:
                print(f"\n📊 Found {len(result['results'])} pages:")
                for page in result['results']:
                    title = page.get('title', 'N/A')
                    page_id = page.get('id', 'N/A')
                    print(f"  • [{page_id}] {title}")
                    
                    # Show URL if available
                    if '_links' in page and 'webui' in page['_links']:
                        webui = page['_links']['webui']
                        print(f"    URL: https://labcollab.aka.corp.amazon.com{webui}")
            else:
                print(f"\n⚠️  No 'results' key in response")
                print(f"Keys: {list(result.keys())}")
                print(f"Result: {result}")
        else:
            print(f"\n⚠️  Result is not a dict: {result}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Search for "test" (more common term)
    print("\n\n📋 Test 2: Search LabCollab for 'test'")
    print("-" * 70)
    
    try:
        result = client.mcp.call_tool(
            "lab_collab_confluence_search_pages",
            {
                "query": "text ~ 'test'",
                "limit": 3
            }
        )
        
        if isinstance(result, dict) and 'results' in result:
            print(f"✅ Found {len(result['results'])} pages:")
            for page in result['results']:
                title = page.get('title', 'N/A')
                print(f"  • {title[:60]}...")
        else:
            print(f"⚠️  Unexpected result format")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get a specific page (if we found one)
    print("\n\n📋 Test 3: Get page content")
    print("-" * 70)
    
    try:
        # First search to get a page ID
        search_result = client.mcp.call_tool(
            "lab_collab_confluence_search_pages",
            {
                "query": "text ~ 'test'",
                "limit": 1
            }
        )
        
        if isinstance(search_result, dict) and 'results' in search_result and len(search_result['results']) > 0:
            page_id = search_result['results'][0]['id']
            page_title = search_result['results'][0]['title']
            
            print(f"Getting page: {page_title} (ID: {page_id})")
            
            # Get the page content
            page_result = client.mcp.call_tool(
                "lab_collab_confluence_get_page",
                {
                    "pageId": page_id,
                    "format": "markdown"
                }
            )
            
            if isinstance(page_result, str):
                print(f"✅ Got page content ({len(page_result)} chars)")
                print(f"\nFirst 200 chars:")
                print(page_result[:200])
            else:
                print(f"⚠️  Unexpected page result type: {type(page_result)}")
        else:
            print("⚠️  No pages found to test with")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Test complete!")

if __name__ == "__main__":
    main()
