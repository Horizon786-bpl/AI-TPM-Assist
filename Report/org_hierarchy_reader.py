#!/usr/bin/env python3
"""
Automated Organizational Hierarchy Reader for Amazon Phonetool

This script reads the complete reporting structure starting from a given user.
It recursively traverses all direct reports and builds a comprehensive org tree.

Usage:
    Run this through Kiro which has MCP access to internal Amazon tools.
"""

import json
import re
from typing import Dict, List, Set
from collections import defaultdict


class OrgHierarchyReader:
    """Reads and processes organizational hierarchy from Phonetool."""
    
    def __init__(self):
        self.visited = set()
        self.org_data = {}
        self.errors = []
    
    def fetch_user_page(self, username: str) -> str:
        """
        Fetch phonetool page for a user.
        This will be called via Kiro's MCP integration.
        """
        # Placeholder - actual implementation uses MCP tool
        # mcp_builder_mcp_ReadInternalWebsites
        return ""
    
    def parse_user_info(self, content: str, username: str) -> Dict:
        """Extract user information from phonetool HTML content."""
        info = {
            "username": username,
            "name": "",
            "title": "",
            "level": "",
            "manager": "",
            "building": "",
            "direct_reports": [],
            "total_reports": 0
        }
        
        # Extract name (usually in page title or header)
        name_patterns = [
            r'<title>([^<]+?)\s*-\s*PhoneTool',
            r'<h1[^>]*>([^<]+)</h1>',
            r'"name"\s*:\s*"([^"]+)"'
        ]
        for pattern in name_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                info["name"] = match.group(1).strip()
                break
        
        # Extract title/job title
        title_patterns = [
            r'(?:Job Title|Title)["\s:]+([^<"\n]+)',
            r'"jobTitle"\s*:\s*"([^"]+)"',
            r'<span[^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</span>'
        ]
        for pattern in title_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                info["title"] = match.group(1).strip()
                break
        
        # Extract level
        level_match = re.search(r'(?:Level|L)[\s:]+(\d+|[IVX]+)', content, re.IGNORECASE)
        if level_match:
            info["level"] = level_match.group(1).strip()
        
        # Extract manager
        manager_patterns = [
            r'Manager["\s:]+<a[^>]+href="/users/([^"]+)"',
            r'"manager"\s*:\s*"([^"]+)"'
        ]
        for pattern in manager_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                info["manager"] = match.group(1).strip()
                break
        
        # Extract direct reports
        # Look for links in the direct reports section
        direct_reports_section = re.search(
            r'(?:Direct Reports?|Reports to|Team Members?)(.*?)(?:<h\d|<div class="section"|$)',
            content,
            re.IGNORECASE | re.DOTALL
        )
        
        if direct_reports_section:
            section_content = direct_reports_section.group(1)
            # Find all user links in this section
            user_links = re.findall(r'/users/([a-z0-9]+)', section_content, re.IGNORECASE)
            info["direct_reports"] = list(set(user_links))  # Remove duplicates
        
        # Try to get total report count
        total_match = re.search(r'(\d+)\s+(?:total\s+)?(?:direct\s+)?reports?', content, re.IGNORECASE)
        if total_match:
            info["total_reports"] = int(total_match.group(1))
        else:
            info["total_reports"] = len(info["direct_reports"])
        
        return info
    
    def build_hierarchy(self, username: str, depth: int = 0, max_depth: int = 10) -> Dict:
        """
        Recursively build organizational hierarchy.
        
        Args:
            username: User login to start from
            depth: Current recursion depth
            max_depth: Maximum depth to traverse
        
        Returns:
            Dictionary with user info and nested direct reports
        """
        # Prevent infinite loops and limit depth
        if username in self.visited or depth >= max_depth:
            return None
        
        self.visited.add(username)
        indent = "  " * depth
        print(f"{indent}📍 Fetching: {username} (depth {depth})")
        
        # Fetch user page (via MCP in actual execution)
        try:
            content = self.fetch_user_page(username)
            if not content:
                print(f"{indent}  ⚠️  No content retrieved")
                return None
            
            # Parse user information
            user_info = self.parse_user_info(content, username)
            print(f"{indent}  ✓ {user_info['name']} - {user_info['title']}")
            print(f"{indent}    Direct reports: {len(user_info['direct_reports'])}")
            
            # Store in org data
            self.org_data[username] = user_info
            
            # Recursively fetch direct reports
            nested_reports = []
            for report_username in user_info['direct_reports']:
                report_tree = self.build_hierarchy(report_username, depth + 1, max_depth)
                if report_tree:
                    nested_reports.append(report_tree)
            
            # Build the tree node
            tree_node = {
                **user_info,
                "direct_reports_tree": nested_reports,
                "depth": depth
            }
            
            return tree_node
            
        except Exception as e:
            error_msg = f"Error processing {username}: {str(e)}"
            print(f"{indent}  ❌ {error_msg}")
            self.errors.append(error_msg)
            return None
    
    def print_tree(self, node: Dict, indent: int = 0, is_last: bool = True):
        """Pretty print the organizational tree."""
        if not node:
            return
        
        prefix = "  " * indent
        connector = "└─" if is_last else "├─"
        
        name = node.get("name") or node["username"]
        title = node.get("title", "")
        level = node.get("level", "")
        report_count = len(node.get("direct_reports_tree", []))
        
        # Main line
        print(f"{prefix}{connector} {name} (@{node['username']})")
        
        # Details
        detail_prefix = prefix + ("   " if is_last else "│  ")
        if title:
            print(f"{detail_prefix}💼 {title}")
        if level:
            print(f"{detail_prefix}📊 Level {level}")
        if report_count > 0:
            print(f"{detail_prefix}👥 {report_count} direct report(s)")
        
        # Recursively print direct reports
        reports = node.get("direct_reports_tree", [])
        for i, report in enumerate(reports):
            is_last_report = (i == len(reports) - 1)
            self.print_tree(report, indent + 1, is_last_report)
    
    def generate_summary(self, tree: Dict) -> Dict:
        """Generate summary statistics from the org tree."""
        def count_nodes(node):
            if not node:
                return 0
            count = 1
            for report in node.get("direct_reports_tree", []):
                count += count_nodes(report)
            return count
        
        def max_depth(node, current_depth=0):
            if not node or not node.get("direct_reports_tree"):
                return current_depth
            depths = [max_depth(r, current_depth + 1) for r in node["direct_reports_tree"]]
            return max(depths) if depths else current_depth
        
        return {
            "total_people": count_nodes(tree),
            "max_depth": max_depth(tree),
            "direct_reports": len(tree.get("direct_reports_tree", [])),
            "root_user": tree.get("username"),
            "root_name": tree.get("name")
        }


def main():
    """Main execution function."""
    print("=" * 80)
    print("🏢 AMAZON ORGANIZATIONAL HIERARCHY READER")
    print("=" * 80)
    print()
    
    # Configuration
    start_username = "jamie"
    max_depth = 5  # Adjust based on how deep you want to go
    
    print(f"Starting user: {start_username}")
    print(f"Maximum depth: {max_depth}")
    print()
    print("⚠️  NOTE: This requires MCP access through Kiro")
    print()
    print("=" * 80)
    print()
    
    # Create reader and build hierarchy
    reader = OrgHierarchyReader()
    
    print("🔍 Building organizational hierarchy...")
    print()
    
    org_tree = reader.build_hierarchy(start_username, max_depth=max_depth)
    
    if org_tree:
        print()
        print("=" * 80)
        print("📊 ORGANIZATIONAL STRUCTURE")
        print("=" * 80)
        print()
        reader.print_tree(org_tree)
        
        # Generate summary
        print()
        print("=" * 80)
        print("📈 SUMMARY STATISTICS")
        print("=" * 80)
        summary = reader.generate_summary(org_tree)
        for key, value in summary.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Save to file
        output_file = f"org_hierarchy_{start_username}.json"
        with open(output_file, "w") as f:
            json.dump(org_tree, f, indent=2)
        print()
        print(f"💾 Full hierarchy saved to: {output_file}")
        
        # Show errors if any
        if reader.errors:
            print()
            print("=" * 80)
            print("⚠️  ERRORS ENCOUNTERED")
            print("=" * 80)
            for error in reader.errors:
                print(f"  • {error}")
    else:
        print()
        print(f"❌ Could not retrieve hierarchy for {start_username}")
        print("   Check authentication and permissions.")
    
    print()
    print("=" * 80)
    print("✅ Complete")
    print("=" * 80)


if __name__ == "__main__":
    main()
