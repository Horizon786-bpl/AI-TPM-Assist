# Status Monitor Bot

Automatically monitors Confluence project status pages and detects changes.

## Purpose

As a TPM, you need to track multiple projects. This bot:
- Reads Confluence status pages automatically
- Extracts key information (status, dates, issues, risks)
- Detects changes from previous reads
- Alerts on status degradation
- Generates executive summaries

## Example Use Case: Flan Project

**Input**: Confluence page URL
```
https://confluence.atl.ring.com/spaces/RCPM/pages/2814198025/Flan
```

**Output**: Structured status report
```json
{
  "project": "Flan",
  "overall_status": "Green",
  "street_date": "2026-04-15",
  "phase": "EVT",
  "key_callouts": [
    "Resource constraints in APP team",
    "Firmware team changes affecting key resources",
    "Phase 2 Alpha trials starting Jan 14"
  ],
  "risks": [
    {
      "description": "APP release delay for Alpha Phase 2",
      "impact": "End-to-end testing delay"
    }
  ],
  "alpha_trials": {
    "devices_setup": 151,
    "setup_rate": "73%",
    "csat_setup": 4.504
  }
}
```

## Features

### MVP (Phase 1)
- [x] Read Confluence page via RBKS MCP
- [ ] Extract structured data (status, dates, metrics)
- [ ] Store historical snapshots
- [ ] Detect status changes
- [ ] Generate summary report

### Future (Phase 2)
- [ ] Monitor multiple projects
- [ ] Scheduled checks (daily/weekly)
- [ ] Slack notifications on changes
- [ ] Trend analysis
- [ ] Predictive alerts

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Status Monitor Bot                                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐    ┌──────────────┐             │
│  │   Reader     │───▶│   Parser     │             │
│  │ (RBKS MCP)   │    │ (Extract)    │             │
│  └──────────────┘    └──────┬───────┘             │
│                              │                      │
│                              ▼                      │
│  ┌──────────────┐    ┌──────────────┐             │
│  │   Storage    │◀───│   Analyzer   │             │
│  │ (History)    │    │ (Detect Δ)   │             │
│  └──────────────┘    └──────┬───────┘             │
│                              │                      │
│                              ▼                      │
│                      ┌──────────────┐              │
│                      │   Reporter   │              │
│                      │ (Summarize)  │              │
│                      └──────────────┘              │
└─────────────────────────────────────────────────────┘
```

## Usage

### Command Line
```bash
# Monitor a single page
python status_monitor.py --url "https://confluence.atl.ring.com/spaces/RCPM/pages/2814198025/Flan"

# Monitor and compare with previous
python status_monitor.py --url "..." --compare

# Generate report
python status_monitor.py --url "..." --report
```

### As a Library
```python
from status_monitor import StatusMonitor

monitor = StatusMonitor()
status = monitor.check_page("2814198025")  # Page ID
print(status.summary())
```

### Integration with Other Bots
```python
# Other bots can subscribe to status changes
from message_bus import MessageBus

bus = MessageBus()
bus.subscribe("status.changed", risk_bot.handle_status_change)
```

## Data Model

### Project Status
```python
@dataclass
class ProjectStatus:
    project_name: str
    page_id: str
    timestamp: datetime
    overall_status: str  # Green/Yellow/Red
    phase: str
    street_date: Optional[date]
    key_callouts: List[str]
    risks: List[Risk]
    metrics: Dict[str, Any]
    raw_content: str
```

### Status Change
```python
@dataclass
class StatusChange:
    project_name: str
    timestamp: datetime
    field: str
    old_value: Any
    new_value: Any
    severity: str  # info/warning/critical
```

## Configuration

```yaml
# config.yaml
projects:
  - name: Flan
    page_id: "2814198025"
    check_frequency: daily
    alert_on:
      - status_degradation
      - date_slip
      - new_risks

storage:
  type: local  # or s3
  path: ./data/history

notifications:
  slack_channel: "#flan-status"
  email: danissid@amazon.com
```

## Next Steps

1. Build MVP parser for Confluence pages
2. Add storage for historical data
3. Implement change detection
4. Add report generation
5. Test with Flan project
6. Expand to other projects
