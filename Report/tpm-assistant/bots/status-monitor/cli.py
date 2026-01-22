#!/usr/bin/env python3
"""
CLI for Status Monitor Bot

This provides a command-line interface to test the bot with RBKS MCP.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from status_monitor import StatusMonitor


def main():
    parser = argparse.ArgumentParser(
        description="Status Monitor Bot - Monitor Confluence project status pages"
    )
    
    parser.add_argument(
        "--content-file",
        help="Path to file containing Confluence markdown content",
        required=True
    )
    
    parser.add_argument(
        "--page-id",
        help="Confluence page ID",
        required=True
    )
    
    parser.add_argument(
        "--project-name",
        help="Project name (optional, will be extracted from content if not provided)"
    )
    
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare with previous version and show changes"
    )
    
    parser.add_argument(
        "--storage-path",
        default="./data/history",
        help="Path to store historical data (default: ./data/history)"
    )
    
    args = parser.parse_args()
    
    # Read content from file
    try:
        with open(args.content_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.content_file}")
        return 1
    except Exception as e:
        print(f"Error reading file: {e}")
        return 1
    
    # Initialize monitor
    monitor = StatusMonitor(storage_path=args.storage_path)
    
    # Check page
    if args.compare:
        status, changes = monitor.check_for_changes(
            content,
            args.page_id,
            args.project_name
        )
        
        # Generate report with changes
        report = monitor.generate_report(status, changes)
        print(report)
        
        if changes:
            print("\n" + "="*60)
            print(f"Detected {len(changes)} change(s)")
            print("="*60)
    else:
        status = monitor.check_page(
            content,
            args.page_id,
            args.project_name
        )
        
        # Generate report
        report = monitor.generate_report(status)
        print(report)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
