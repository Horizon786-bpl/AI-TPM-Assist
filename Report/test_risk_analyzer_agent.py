#!/usr/bin/env python3
"""
Test Risk Analyzer Agent directly

This tests the full agent flow:
1. Search Confluence for program
2. Get page content
3. Extract risks
4. Analyze with Claude AI
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tpm-slack-bot', 'src'))

print("="*70)
print("Risk Analyzer Agent Test")
print("="*70)

try:
    logger.info("Importing modules...")
    from services.mcp_client import RBKSMCPClient, MCPConfluenceFetcher
    from services.bedrock_client import BedrockClient
    from agents.risk_analyzer import RiskAnalyzerAgent
    
    logger.info("✅ Imports successful")
    
    logger.info("Initializing clients...")
    rbks_client = RBKSMCPClient()
    confluence_fetcher = MCPConfluenceFetcher(rbks_client)
    bedrock_client = BedrockClient()
    
    logger.info("✅ Clients initialized")
    
    logger.info("Initializing Risk Analyzer Agent...")
    risk_analyzer = RiskAnalyzerAgent(rbks_client, confluence_fetcher, bedrock_client)
    
    logger.info("✅ Agent initialized")
    
    # Test with Hexa
    program_name = "Hexa"
    logger.info(f"\nAnalyzing risks for: {program_name}")
    
    state = {
        'program_name': program_name,
        'agent_results': {}
    }
    
    logger.info("Executing agent...")
    result = risk_analyzer.execute(state)
    
    if result.get('error'):
        print("\n" + "="*70)
        print("❌ Agent returned error:")
        print("="*70)
        print(result['error'])
        sys.exit(1)
    
    # Success!
    analysis = result['agent_results']['risk_analyzer']
    
    print("\n" + "="*70)
    print("✅ SUCCESS! Risk Analysis Complete")
    print("="*70)
    print(f"\nProgram: {analysis['program_name']}")
    print(f"Page: {analysis['page_title']}")
    print(f"URL: {analysis['page_url']}")
    print(f"Status: {analysis['program_status']}")
    print("\n" + "-"*70)
    print("Risk Analysis:")
    print("-"*70)
    print(analysis['risk_analysis'][:500] + "...")
    print("\n" + "="*70)
    print("✅ Agent test passed!")
    print("="*70)
    
except Exception as e:
    logger.error(f"❌ Test failed: {e}", exc_info=True)
    print("\n" + "="*70)
    print("❌ Test Failed")
    print("="*70)
    print(f"\nError: {e}")
    sys.exit(1)
