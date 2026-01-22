#!/usr/bin/env python3
"""
Test RBKS MCP with detailed logging

This will show exactly what's happening when we try to use RBKS MCP.
"""

import sys
import os
import logging

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rbks_mcp_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

print("="*70)
print("RBKS MCP Connection Test with Full Logging")
print("="*70)
print("\nLogs will be saved to: rbks_mcp_test.log")
print()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot', 'src'))

try:
    logger.info("Step 1: Importing RBKSMCPClient...")
    from services.mcp_client import RBKSMCPClient
    logger.info("✅ Import successful")
    
    logger.info("Step 2: Initializing RBKSMCPClient...")
    client = RBKSMCPClient()
    logger.info("✅ Client initialized")
    
    logger.info("Step 3: Searching Confluence for 'Hexa'...")
    results = client.search_confluence_pages(query='text ~ "Hexa"', limit=5)
    logger.info(f"✅ Search completed: {len(results)} results")
    
    if results:
        logger.info("First result:")
        logger.info(f"  Title: {results[0].get('title')}")
        logger.info(f"  ID: {results[0].get('id')}")
        logger.info(f"  URL: {results[0].get('url')}")
        
        print("\n" + "="*70)
        print("✅ SUCCESS! RBKS MCP is working!")
        print("="*70)
        print(f"\nFound {len(results)} pages:")
        for r in results:
            print(f"  • {r.get('title')}")
    else:
        logger.warning("⚠️  Search returned no results")
        print("\n" + "="*70)
        print("⚠️  RBKS MCP connected but returned no results")
        print("="*70)
    
except Exception as e:
    logger.error(f"❌ Error: {e}", exc_info=True)
    print("\n" + "="*70)
    print("❌ RBKS MCP Test Failed")
    print("="*70)
    print(f"\nError: {e}")
    print("\nCheck rbks_mcp_test.log for full details")
    sys.exit(1)

print("\n✅ Test complete. Check rbks_mcp_test.log for full details.")
