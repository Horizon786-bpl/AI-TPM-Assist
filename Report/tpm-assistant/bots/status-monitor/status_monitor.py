"""
Status Monitor Bot - Tracks Confluence project status pages

This bot reads Confluence pages via RBKS MCP, extracts structured data,
and detects changes over time.
"""

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class Risk:
    """Represents a project risk"""
    description: str
    owner: Optional[str] = None
    eta: Optional[str] = None
    status: Optional[str] = None
    comment: Optional[str] = None


@dataclass
class ProjectStatus:
    """Represents the current status of a project"""
    project_name: str
    page_id: str
    timestamp: datetime
    overall_status: str  # Green/Yellow/Red
    phase: Optional[str] = None
    street_date: Optional[str] = None
    mp_date: Optional[str] = None
    key_callouts: List[str] = None
    risks: List[Risk] = None
    metrics: Dict[str, Any] = None
    raw_content: str = ""
    
    def __post_init__(self):
        if self.key_callouts is None:
            self.key_callouts = []
        if self.risks is None:
            self.risks = []
        if self.metrics is None:
            self.metrics = {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProjectStatus':
        """Create from dictionary"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        if data.get('risks'):
            data['risks'] = [Risk(**r) if isinstance(r, dict) else r for r in data['risks']]
        return cls(**data)


@dataclass
class StatusChange:
    """Represents a change in project status"""
    project_name: str
    timestamp: datetime
    field: str
    old_value: Any
    new_value: Any
    severity: str  # info/warning/critical
    
    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.field}: {self.old_value} → {self.new_value}"


class StatusParser:
    """Parses Confluence markdown content to extract structured status"""
    
    @staticmethod
    def extract_status(content: str) -> str:
        """Extract overall status (Green/Yellow/Red)"""
        # Look for status indicators
        patterns = [
            r'\*\*Green\*\*',
            r'\*\*Yellow\*\*',
            r'\*\*Red\*\*',
            r'StatusINLINE\*\*Green\*\*',
            r'StatusINLINE\*\*Yellow\*\*',
            r'StatusINLINE\*\*Red\*\*',
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                if 'Green' in pattern:
                    return 'Green'
                elif 'Yellow' in pattern:
                    return 'Yellow'
                elif 'Red' in pattern:
                    return 'Red'
        
        return 'Unknown'
    
    @staticmethod
    def extract_dates(content: str) -> Dict[str, Optional[str]]:
        """Extract key dates (street date, MP date)"""
        dates = {
            'street_date': None,
            'mp_date': None
        }
        
        # Street date patterns
        street_patterns = [
            r'Street[:\s]+(\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})',
            r'Street Date[:\s]+(\d{1,2}(?:st|nd|rd|th)?\s+\w+)',
            r'Street.*?(\d{4}-\d{2}-\d{2})',
        ]
        
        for pattern in street_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                dates['street_date'] = match.group(1)
                break
        
        # MP date patterns
        mp_patterns = [
            r'MP[:\s]+(\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})',
            r'MP.*?(\d{4}-\d{2}-\d{2})',
        ]
        
        for pattern in mp_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                dates['mp_date'] = match.group(1)
                break
        
        return dates
    
    @staticmethod
    def extract_phase(content: str) -> Optional[str]:
        """Extract current phase (EVT, DVT, PVT, etc.)"""
        phase_patterns = [
            r'Phase[:\s]+.*?(EVT|DVT|PVT|MP)',
            r'Subphase[:\s]+.*?(EVT|DVT|PVT|MP)',
        ]
        
        for pattern in phase_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        
        return None
    
    @staticmethod
    def extract_key_callouts(content: str) -> List[str]:
        """Extract key callouts from executive summary"""
        callouts = []
        
        # Look for executive summary section
        exec_summary_match = re.search(
            r'Executive Summary.*?(?=\n#|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if exec_summary_match:
            summary_text = exec_summary_match.group(0)
            
            # Extract sentences that indicate issues or important points
            keywords = [
                'resource constraint',
                'risk',
                'delay',
                'critical',
                'impact',
                'mitigation',
                'blocker',
                'issue'
            ]
            
            sentences = re.split(r'[.!?]+', summary_text)
            for sentence in sentences:
                sentence = sentence.strip()
                if any(keyword in sentence.lower() for keyword in keywords):
                    if len(sentence) > 20:  # Filter out too short
                        callouts.append(sentence)
        
        return callouts[:5]  # Limit to top 5
    
    @staticmethod
    def extract_risks(content: str) -> List[Risk]:
        """Extract risks from risk tables"""
        risks = []
        
        # Look for risk/issue tables
        # This is a simplified parser - can be enhanced
        risk_section_match = re.search(
            r'(?:Key Open Issues|Risks?/Issues?).*?\n\|.*?\n\|(.*?)(?=\n#|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if risk_section_match:
            table_content = risk_section_match.group(1)
            rows = table_content.split('\n|')
            
            for row in rows:
                if row.strip() and not row.strip().startswith('-'):
                    cells = [cell.strip() for cell in row.split('|')]
                    if len(cells) >= 2 and cells[0]:
                        risk = Risk(
                            description=cells[0],
                            owner=cells[1] if len(cells) > 1 else None,
                            eta=cells[2] if len(cells) > 2 else None,
                            status=cells[3] if len(cells) > 3 else None,
                            comment=cells[4] if len(cells) > 4 else None
                        )
                        risks.append(risk)
        
        return risks
    
    @staticmethod
    def extract_metrics(content: str) -> Dict[str, Any]:
        """Extract numerical metrics (setup rate, CSAT, etc.)"""
        metrics = {}
        
        # Alpha trials metrics
        setup_match = re.search(r'(\d+)\s*\((\d+)%\)\s*(?:trials\s*)?devices?\s*(?:have\s*been\s*)?set\s*up', content, re.IGNORECASE)
        if setup_match:
            metrics['alpha_devices_setup'] = int(setup_match.group(1))
            metrics['alpha_setup_rate'] = f"{setup_match.group(2)}%"
        
        # CSAT scores
        csat_patterns = [
            (r'setup.*?(\d+\.\d+)/5', 'csat_setup'),
            (r'response\s*time.*?(\d+\.\d+)/5', 'csat_response_time'),
            (r'audio\s*quality.*?(\d+\.\d+)/5', 'csat_audio_quality'),
        ]
        
        for pattern, key in csat_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                metrics[key] = float(match.group(1))
        
        return metrics
    
    def parse(self, content: str, page_id: str, project_name: str = None) -> ProjectStatus:
        """Parse Confluence content into structured ProjectStatus"""
        
        # Extract project name from content if not provided
        if not project_name:
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                project_name = title_match.group(1).strip()
            else:
                project_name = "Unknown Project"
        
        status = ProjectStatus(
            project_name=project_name,
            page_id=page_id,
            timestamp=datetime.now(),
            overall_status=self.extract_status(content),
            phase=self.extract_phase(content),
            key_callouts=self.extract_key_callouts(content),
            risks=self.extract_risks(content),
            metrics=self.extract_metrics(content),
            raw_content=content
        )
        
        # Extract dates
        dates = self.extract_dates(content)
        status.street_date = dates['street_date']
        status.mp_date = dates['mp_date']
        
        return status


class StatusStorage:
    """Stores and retrieves historical status data"""
    
    def __init__(self, storage_path: str = "./data/history"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, status: ProjectStatus):
        """Save status snapshot"""
        project_dir = self.storage_path / status.project_name.replace(" ", "_")
        project_dir.mkdir(exist_ok=True)
        
        filename = f"{status.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = project_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(status.to_dict(), f, indent=2)
    
    def get_latest(self, project_name: str) -> Optional[ProjectStatus]:
        """Get most recent status for a project"""
        project_dir = self.storage_path / project_name.replace(" ", "_")
        
        if not project_dir.exists():
            return None
        
        files = sorted(project_dir.glob("*.json"), reverse=True)
        if not files:
            return None
        
        with open(files[0], 'r') as f:
            data = json.load(f)
            return ProjectStatus.from_dict(data)
    
    def get_history(self, project_name: str, limit: int = 10) -> List[ProjectStatus]:
        """Get historical status snapshots"""
        project_dir = self.storage_path / project_name.replace(" ", "_")
        
        if not project_dir.exists():
            return []
        
        files = sorted(project_dir.glob("*.json"), reverse=True)[:limit]
        history = []
        
        for file in files:
            with open(file, 'r') as f:
                data = json.load(f)
                history.append(ProjectStatus.from_dict(data))
        
        return history


class StatusAnalyzer:
    """Analyzes status changes and generates insights"""
    
    @staticmethod
    def detect_changes(old_status: ProjectStatus, new_status: ProjectStatus) -> List[StatusChange]:
        """Detect changes between two status snapshots"""
        changes = []
        
        # Check overall status change
        if old_status.overall_status != new_status.overall_status:
            severity = StatusAnalyzer._get_status_change_severity(
                old_status.overall_status,
                new_status.overall_status
            )
            changes.append(StatusChange(
                project_name=new_status.project_name,
                timestamp=new_status.timestamp,
                field="overall_status",
                old_value=old_status.overall_status,
                new_value=new_status.overall_status,
                severity=severity
            ))
        
        # Check date changes
        if old_status.street_date != new_status.street_date:
            changes.append(StatusChange(
                project_name=new_status.project_name,
                timestamp=new_status.timestamp,
                field="street_date",
                old_value=old_status.street_date,
                new_value=new_status.street_date,
                severity="warning"
            ))
        
        # Check phase changes
        if old_status.phase != new_status.phase:
            changes.append(StatusChange(
                project_name=new_status.project_name,
                timestamp=new_status.timestamp,
                field="phase",
                old_value=old_status.phase,
                new_value=new_status.phase,
                severity="info"
            ))
        
        # Check for new risks
        old_risk_count = len(old_status.risks)
        new_risk_count = len(new_status.risks)
        if new_risk_count > old_risk_count:
            changes.append(StatusChange(
                project_name=new_status.project_name,
                timestamp=new_status.timestamp,
                field="risks",
                old_value=f"{old_risk_count} risks",
                new_value=f"{new_risk_count} risks",
                severity="warning"
            ))
        
        return changes
    
    @staticmethod
    def _get_status_change_severity(old: str, new: str) -> str:
        """Determine severity of status change"""
        status_order = {'Green': 0, 'Yellow': 1, 'Red': 2, 'Unknown': 3}
        
        old_level = status_order.get(old, 3)
        new_level = status_order.get(new, 3)
        
        if new_level > old_level:
            return "critical"  # Degradation
        elif new_level < old_level:
            return "info"  # Improvement
        else:
            return "info"  # No change


class StatusMonitor:
    """Main Status Monitor Bot"""
    
    def __init__(self, storage_path: str = "./data/history"):
        self.parser = StatusParser()
        self.storage = StatusStorage(storage_path)
        self.analyzer = StatusAnalyzer()
    
    def check_page(self, page_content: str, page_id: str, project_name: str = None) -> ProjectStatus:
        """
        Check a Confluence page and return structured status
        
        Args:
            page_content: Markdown content from Confluence
            page_id: Confluence page ID
            project_name: Optional project name override
        
        Returns:
            ProjectStatus object
        """
        # Parse the content
        status = self.parser.parse(page_content, page_id, project_name)
        
        # Save to history
        self.storage.save(status)
        
        return status
    
    def check_for_changes(self, page_content: str, page_id: str, project_name: str = None) -> tuple[ProjectStatus, List[StatusChange]]:
        """
        Check page and detect changes from previous version
        
        Returns:
            Tuple of (current_status, list_of_changes)
        """
        # Get current status
        current_status = self.parser.parse(page_content, page_id, project_name)
        
        # Get previous status
        previous_status = self.storage.get_latest(current_status.project_name)
        
        # Detect changes
        changes = []
        if previous_status:
            changes = self.analyzer.detect_changes(previous_status, current_status)
        
        # Save current status
        self.storage.save(current_status)
        
        return current_status, changes
    
    def generate_report(self, status: ProjectStatus, changes: List[StatusChange] = None) -> str:
        """Generate a human-readable status report"""
        report = []
        report.append(f"# {status.project_name} Status Report")
        report.append(f"Generated: {status.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall status
        status_emoji = {"Green": "🟢", "Yellow": "🟡", "Red": "🔴", "Unknown": "⚪"}
        report.append(f"## Overall Status: {status_emoji.get(status.overall_status, '⚪')} {status.overall_status}")
        report.append("")
        
        # Key info
        if status.phase:
            report.append(f"**Phase**: {status.phase}")
        if status.street_date:
            report.append(f"**Street Date**: {status.street_date}")
        if status.mp_date:
            report.append(f"**MP Date**: {status.mp_date}")
        report.append("")
        
        # Changes
        if changes:
            report.append("## Changes Detected")
            for change in changes:
                severity_emoji = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨"}
                report.append(f"- {severity_emoji.get(change.severity, 'ℹ️')} {change}")
            report.append("")
        
        # Key callouts
        if status.key_callouts:
            report.append("## Key Callouts")
            for callout in status.key_callouts:
                report.append(f"- {callout}")
            report.append("")
        
        # Risks
        if status.risks:
            report.append("## Open Risks/Issues")
            for risk in status.risks[:5]:  # Top 5
                report.append(f"- **{risk.description}**")
                if risk.owner:
                    report.append(f"  - Owner: {risk.owner}")
                if risk.eta:
                    report.append(f"  - ETA: {risk.eta}")
            report.append("")
        
        # Metrics
        if status.metrics:
            report.append("## Key Metrics")
            for key, value in status.metrics.items():
                formatted_key = key.replace('_', ' ').title()
                report.append(f"- {formatted_key}: {value}")
            report.append("")
        
        return "\n".join(report)


if __name__ == "__main__":
    # Example usage
    print("Status Monitor Bot - Ready")
    print("Use this bot with RBKS MCP to monitor Confluence pages")
