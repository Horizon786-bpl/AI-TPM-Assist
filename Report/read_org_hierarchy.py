#!/usr/bin/env python3
"""
Script to read and display organizational hierarchy from Amazon Phonetool.
Recursively traverses reporting lines starting from a given user.
"""

import json
import re
from typing import Dict, List, Set, Optional


def get_user_info(username: str) -> Optional[str]:
    """Fetch user information from Phonetool - returns raw content."""
    print(f"  → Fetching phonetool data for: {username}")
    # This will be called via Kiro's MCP integration
    # For now, return None to indicate manual MCP call needed
    return None


def extract_direct_reports(content: str) -> List[str]:
    """Extract list of direct report usernames from phonetool content."""
    direct_reports = []
    
    # Look for patterns like /users/username or phonetool links
    # Common patterns in phonetool HTML:
    # - <a href="/users/username">
    # - phonetool.amazon.com/users/username
    
    patterns = [
        r'/users/([a-z0-9]+)',
        r'phonetool\.amazon\.com/users/([a-z0-9]+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        direct_reports.extend(matches)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_reports = []
    for report in direct_reports:
        if report not in seen:
            seen.add(report)
            unique_reports.append(report)
    
    return unique_reports


def extract_user_details(content: str, username: str) -> Dict:
    """Extract user details from phonetool content."""
    details = {
        "username": username,
        "name": None,
        "title": None,
        "manager": None,
        "level": None,
        "building": None,
    }
    
    # Try to extract name (usually in title or h1)
    name_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    if name_match:
        details["name"] = name_match.group(1).strip()
    
    # Try to extract title
    title_match = re.search(r'(?:title|position)["\s:]+([^<"\n]+)', content, re.IGNORECASE)
    if title_match:
        details["title"] = title_match.group(1).strip()
    
    return details


def print_org_tree(node: Dict, indent: int = 0):
    """Pretty print the organizational tree."""
    if not node:
        return
    
    prefix = "  " * indent
    name = node.get("name") or node["username"]
    title = node.get("title", "")
    level = node.get("level", "")
    
    print(f"{prefix}├─ {name} ({node['username']})")
    if title:
        print(f"{prefix}│  Title: {title}")
    if level:
        print(f"{prefix}│  Level: {level}")
    
    direct_reports = node.get("direct_reports", [])
    if direct_reports:
        print(f"{prefix}│  Direct Reports: {len(direct_reports)}")
    
    for i, report in enumerate(direct_reports):
        is_last = (i == len(direct_reports) - 1)
        print_org_tree(report, indent + 1)


def main():
    """
    Main execution - provides instructions for manual hierarchy reading.
    
    Since this requires MCP tool access through Kiro, we'll provide
    a step-by-step guide for reading the hierarchy.
    """
    username = "jamie"
    
    print(f"📋 Organizational Hierarchy Reader for: {username}")
    print("=" * 80)
    print()
    print("This script will help you read the reporting structure from Phonetool.")
    print()
    print("INSTRUCTIONS:")
    print("1. I'll fetch the phonetool page for jamie")
    print("2. Extract direct reports from the page")
    print("3. Recursively fetch each direct report's page")
    print("4. Build a complete organizational tree")
    print()
    print("Starting automated hierarchy scan...")
    print("=" * 80)
    print()
    
    # The actual fetching will be done via Kiro's MCP tools
    print(f"Ready to fetch: https://phonetool.amazon.com/users/{username}")
    print()
    print("Please run this script through Kiro to enable MCP tool access.")


if __name__ == "__main__":
    main()
