# Design Document

## Overview

The Confluence-Jira Automation System is a modular Python application that automates the weekly status update process for TPMs at Ring. The system authenticates with Amazon's Midway system, reads Confluence pages, summarizes linked documents using AI, extracts status indicators, and integrates Jira project data into a consolidated Confluence page.

The design follows a modular architecture with clear separation of concerns:
- **Authentication Module**: Handles Midway authentication via Chrome remote debugging
- **Confluence Module**: Manages page fetching, parsing, and updates
- **Summarization Module**: Generates AI-powered summaries of module pages
- **Jira Module**: Fetches and formats Jira project data
- **Orchestration Module**: Coordinates the workflow across all modules

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (CLI)                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                  Orchestration Module                        │
│  - Workflow coordination                                     │
│  - Progress tracking                                         │
│  - Error aggregation                                         │
└─┬────────┬────────┬────────┬────────┬──────────────────────┘
  │        │        │        │        │
  ▼        ▼        ▼        ▼        ▼
┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────────┐
│Auth│  │Conf│  │Summ│  │Jira│  │Storage │
│    │  │    │  │    │  │    │  │        │
└────┘  └────┘  └────┘  └────┘  └────────┘
  │        │        │        │        │
  └────────┴────────┴────────┴────────┘
                   │
         ┌─────────▼──────────┐
         │  Chrome Browser    │
         │  (Remote Debugging)│
         └────────────────────┘
```

### Module Interactions

1. **Authentication Flow**: Orchestrator → Auth Module → Chrome → Midway → Cookies
2. **Page Fetch Flow**: Orchestrator → Confluence Module → Auth Module → HTTP Client
3. **Summarization Flow**: Orchestrator → Summarization Module → AI Service (Bedrock/OpenAI)
4. **Jira Flow**: Orchestrator → Jira Module → Auth Module → Jira API
5. **Update Flow**: Orchestrator → Confluence Module → Auth Module → Confluence API

## Components and Interfaces

### 1. Authentication Module (`auth_manager.py`)

**Responsibility**: Manage Midway authentication and session cookies

**Key Classes**:

```python
class ChromeDebugger:
    """Manages Chrome remote debugging connection"""
    def __init__(self, debug_port: int = 9222)
    def start_chrome(self) -> bool
    def connect_to_chrome(self) -> webdriver.Chrome
    def is_chrome_running(self) -> bool

class MidwayAuthenticator:
    """Handles Midway authentication flow"""
    def __init__(self, chrome_debugger: ChromeDebugger)
    def authenticate(self, confluence_url: str) -> Dict[str, str]
    def wait_for_authentication(self, timeout: int = 300) -> bool
    def extract_cookies(self) -> Dict[str, str]
    def validate_cookies(self, cookies: Dict[str, str]) -> bool
```

**Interface**:
- Input: Confluence URL
- Output: Dictionary of authenticated cookies
- Errors: `AuthenticationError`, `ChromeConnectionError`

### 2. Confluence Module (`confluence_manager.py`)

**Responsibility**: Fetch, parse, and update Confluence pages

**Key Classes**:

```python
class ConfluenceClient:
    """HTTP client for Confluence API"""
    def __init__(self, base_url: str, cookies: Dict[str, str])
    def fetch_page(self, page_id: str) -> str
    def update_page(self, page_id: str, content: str, version: int) -> bool
    def fetch_page_with_retry(self, url: str, max_retries: int = 3) -> str

class ConfluenceParser:
    """Parses Confluence HTML content"""
    def __init__(self, html_content: str)
    def find_section(self, section_number: str) -> BeautifulSoup
    def parse_table(self, section: BeautifulSoup) -> List[ModuleRow]
    def extract_module_rows(self) -> List[ModuleRow]

class ConfluenceUpdater:
    """Updates Confluence page content"""
    def __init__(self, client: ConfluenceClient, parser: ConfluenceParser)
    def update_module_summary(self, module: str, summary: str) -> bool
    def update_module_status(self, module: str, status: str) -> bool
    def update_comprehensive_summary(self, summary: str) -> bool
    def create_jira_section(self, jira_table: str) -> bool
```

**Data Models**:

```python
@dataclass
class ModuleRow:
    module_name: str
    link_url: str
    current_status: str
    owner: str
    current_summary: str
```

### 3. Summarization Module (`summarizer.py`)

**Responsibility**: Generate AI-powered summaries of module pages

**Key Classes**:

```python
class ContentExtractor:
    """Extracts main content from HTML pages"""
    def __init__(self, html_content: str)
    def extract_main_content(self) -> str
    def remove_navigation(self) -> str
    def extract_status_section(self) -> Optional[str]

class StatusDetector:
    """Detects status indicators from content"""
    def __init__(self, content: str)
    def find_status_indicator(self) -> Optional[str]
    def infer_status_from_keywords(self) -> str
    def map_to_standard_color(self, status: str) -> str

class AISummarizer:
    """Generates AI summaries using Bedrock/OpenAI"""
    def __init__(self, api_key: str, model: str = "claude-3-sonnet")
    def summarize_module(self, content: str, module_name: str) -> str
    def generate_comprehensive_summary(self, summaries: List[ModuleSummary]) -> str
    def _build_prompt(self, content: str, module_name: str) -> str
```

**Data Models**:

```python
@dataclass
class ModuleSummary:
    module_name: str
    summary: str
    status: str
    link_url: str
```

### 4. Jira Module (`jira_manager.py`)

**Responsibility**: Fetch and format Jira project data

**Key Classes**:

```python
class JiraClient:
    """HTTP client for Jira API"""
    def __init__(self, base_url: str, cookies: Dict[str, str])
    def fetch_project_issues(self, project_key: str) -> List[JiraIssue]
    def validate_project(self, project_key: str) -> bool
    def extract_project_key_from_url(self, url: str) -> str

class JiraTableGenerator:
    """Generates Confluence table from Jira data"""
    def __init__(self, issues: List[JiraIssue])
    def generate_table_html(self, max_issues: int = 50) -> str
    def group_by_status(self) -> Dict[str, List[JiraIssue]]
    def filter_high_priority(self) -> List[JiraIssue]
```

**Data Models**:

```python
@dataclass
class JiraIssue:
    key: str
    summary: str
    status: str
    assignee: str
    priority: str
    url: str
```

### 5. Orchestration Module (`orchestrator.py`)

**Responsibility**: Coordinate the entire workflow

**Key Classes**:

```python
class WorkflowOrchestrator:
    """Coordinates the automation workflow"""
    def __init__(self, config: Config)
    def run(self) -> WorkflowResult
    def phase1_authenticate(self) -> Dict[str, str]
    def phase2_fetch_and_parse(self) -> List[ModuleRow]
    def phase3_summarize_modules(self, modules: List[ModuleRow]) -> List[ModuleSummary]
    def phase4_jira_integration(self) -> Optional[str]
    def phase5_update_confluence(self, summaries: List[ModuleSummary], jira_table: Optional[str]) -> bool

class ProgressTracker:
    """Tracks and displays progress"""
    def __init__(self, total_modules: int)
    def update(self, module_name: str, status: str)
    def display_summary(self)
```

**Data Models**:

```python
@dataclass
class WorkflowResult:
    success: bool
    modules_processed: int
    modules_failed: int
    failed_modules: List[str]
    jira_integrated: bool
    output_file: str
```

## Data Models

### Core Data Structures

```python
@dataclass
class Config:
    """Application configuration"""
    confluence_base_url: str
    page_id: str
    section_number: str
    link_column: str
    summary_column: str
    status_column: str
    chrome_debug_port: int
    ai_model: str
    ai_api_key: str
    jira_base_url: str
    max_retries: int
    retry_delay: int

@dataclass
class ModuleRow:
    """Represents a row in the Functional Status Update table"""
    module_name: str
    link_url: str
    current_status: str
    owner: str
    current_summary: str

@dataclass
class ModuleSummary:
    """Summary generated for a module"""
    module_name: str
    summary: str
    status: str
    link_url: str

@dataclass
class JiraIssue:
    """Represents a Jira issue"""
    key: str
    summary: str
    status: str
    assignee: str
    priority: str
    url: str

@dataclass
class WorkflowResult:
    """Result of the automation workflow"""
    success: bool
    modules_processed: int
    modules_failed: int
    failed_modules: List[str]
    jira_integrated: bool
    output_file: str
```



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Chrome Connection Consistency

*For any* system configuration with a valid debug port, when the system starts, it should successfully establish a connection to Chrome or launch Chrome with debugging enabled.
**Validates: Requirements 1.1**

### Property 2: Cookie Extraction Completeness

*For any* authenticated browser session, when cookies are extracted, all required Midway authentication cookies should be present in the extracted cookie dictionary.
**Validates: Requirements 1.4, 1.5**

### Property 3: Section Parsing Accuracy

*For any* valid Confluence HTML page with numbered sections, when parsing for a specific section number, the parser should return the correct section content.
**Validates: Requirements 2.1**

### Property 4: Table Row Extraction Completeness

*For any* HTML table with valid structure, when parsing table rows, the parser should extract all non-empty rows with their complete metadata (module name, link, status, owner).
**Validates: Requirements 2.2, 2.3, 2.5**

### Property 5: Authenticated Request Propagation

*For any* HTTP request made after authentication, the request should include all extracted authentication cookies.
**Validates: Requirements 3.1, 7.1**

### Property 6: Content Extraction Cleanliness

*For any* HTML page, when extracting main content, the result should not contain navigation elements, headers, or footers.
**Validates: Requirements 3.2**

### Property 7: Retry Logic Consistency

*For any* failed HTTP request, the system should retry exactly 3 times with exponential backoff delays before marking as failed.
**Validates: Requirements 3.5, 7.5, 10.4**

### Property 8: Status Detection Normalization

*For any* content containing status indicators (explicit or inferred), the detected status should map to exactly one of the standard colors: Green, Yellow, or Red.
**Validates: Requirements 4.1, 4.2, 4.3, 4.4**

### Property 9: Comprehensive Summary Length

*For any* set of module summaries, the generated comprehensive summary should contain between 3 and 4 sentences.
**Validates: Requirements 5.3**

### Property 10: Red Status Highlighting

*For any* set of module summaries containing at least one Red status, the comprehensive summary should explicitly mention the red status modules.
**Validates: Requirements 5.4**

### Property 11: Jira URL Parsing Correctness

*For any* valid Jira URL, the project key extraction should return a non-empty string matching the Jira project key format (uppercase letters and numbers).
**Validates: Requirements 6.2**

### Property 12: Jira Issue Extraction Completeness

*For any* Jira API response containing issues, all issues should be extracted with complete metadata (key, summary, status, assignee, priority).
**Validates: Requirements 7.3**

### Property 13: Issue Grouping Correctness

*For any* list of Jira issues, when grouped by status, each issue should appear in exactly one status group.
**Validates: Requirements 7.4**

### Property 14: Jira Table Structure Validity

*For any* generated Jira table HTML, the table should contain exactly 5 columns (Issue Key, Summary, Status, Assignee, Priority) and one row per issue.
**Validates: Requirements 8.2, 8.3**

### Property 15: High-Priority Filtering

*For any* list of Jira issues exceeding 50 items, the filtered table should contain only high-priority issues and the count should not exceed 50.
**Validates: Requirements 8.4**

### Property 16: Content Preservation

*For any* Confluence page update, all content outside the updated sections (module summaries, status, Jira section) should remain unchanged.
**Validates: Requirements 8.5, 9.2, 9.3, 9.4, 9.5**

### Property 17: Error Logging Completeness

*For any* module processing failure, the error log should contain both the module name and a non-empty failure reason.
**Validates: Requirements 10.1**

### Property 18: Processing Summary Accuracy

*For any* workflow execution, the final summary should report counts where (modules_processed + modules_failed) equals the total number of modules attempted.
**Validates: Requirements 10.2**

### Property 19: Backup File Creation

*For any* failed Confluence update, a local HTML backup file should be created containing all generated content.
**Validates: Requirements 10.5**

### Property 20: Workflow Optional Jira

*For any* workflow execution where Jira integration is skipped, the workflow should complete successfully without Jira data.
**Validates: Requirements 6.5**

## Error Handling

### Error Categories

1. **Authentication Errors**
   - Chrome connection failures
   - Midway authentication timeouts
   - Cookie extraction failures
   - **Handling**: Retry with user guidance, provide clear re-authentication instructions

2. **Network Errors**
   - HTTP request timeouts
   - Connection refused
   - DNS resolution failures
   - **Handling**: Exponential backoff retry (3 attempts), log detailed error information

3. **Parsing Errors**
   - Invalid HTML structure
   - Missing expected sections
   - Malformed table data
   - **Handling**: Log warning, skip problematic item, continue with remaining items

4. **API Errors**
   - Jira API rate limiting
   - Confluence API failures
   - Invalid API responses
   - **Handling**: Exponential backoff, graceful degradation, save backup locally

5. **Data Validation Errors**
   - Invalid Jira project keys
   - Missing required fields
   - Unexpected data formats
   - **Handling**: Validate early, provide clear error messages, allow user correction

### Error Recovery Strategy

```python
class ErrorRecoveryStrategy:
    """Defines recovery strategies for different error types"""
    
    def handle_authentication_error(self, error: AuthenticationError) -> RecoveryAction:
        """Prompt user to re-authenticate"""
        return RecoveryAction.PROMPT_USER
    
    def handle_network_error(self, error: NetworkError, attempt: int) -> RecoveryAction:
        """Retry with exponential backoff"""
        if attempt < 3:
            return RecoveryAction.RETRY_WITH_BACKOFF
        return RecoveryAction.FAIL_AND_LOG
    
    def handle_parsing_error(self, error: ParsingError) -> RecoveryAction:
        """Skip item and continue"""
        return RecoveryAction.SKIP_AND_CONTINUE
    
    def handle_api_error(self, error: APIError) -> RecoveryAction:
        """Save backup and notify user"""
        return RecoveryAction.SAVE_BACKUP_AND_NOTIFY
```

### Logging Strategy

- **Level**: INFO for normal operations, WARNING for recoverable errors, ERROR for failures
- **Format**: `[TIMESTAMP] [LEVEL] [MODULE] [OPERATION] - Message`
- **Destination**: Console output + rotating file log (max 10MB, 5 backups)
- **Sensitive Data**: Mask cookies and authentication tokens in logs

## Testing Strategy

### Unit Testing

Unit tests will verify individual components in isolation:

1. **Authentication Module Tests**
   - Test Chrome connection detection
   - Test cookie extraction from mock browser
   - Test cookie validation logic

2. **Confluence Module Tests**
   - Test HTML parsing with various table structures
   - Test section finding logic
   - Test table row extraction

3. **Summarization Module Tests**
   - Test content extraction with various HTML structures
   - Test status detection with different formats
   - Test status normalization

4. **Jira Module Tests**
   - Test project key extraction from URLs
   - Test issue data extraction from mock API responses
   - Test table HTML generation

5. **Orchestration Module Tests**
   - Test workflow phase coordination
   - Test error aggregation
   - Test progress tracking

### Property-Based Testing

Property-based tests will verify universal properties across many inputs using the `hypothesis` library for Python. Each test will run a minimum of 100 iterations with randomly generated inputs.

1. **Property Test for Chrome Connection** (Property 1)
   - Generate random port numbers
   - Verify connection attempts use correct port
   - **Feature: confluence-jira-automation, Property 1: Chrome Connection Consistency**

2. **Property Test for Cookie Extraction** (Property 2)
   - Generate random authenticated browser states
   - Verify all required cookies are extracted
   - **Feature: confluence-jira-automation, Property 2: Cookie Extraction Completeness**

3. **Property Test for Section Parsing** (Property 3)
   - Generate random HTML with numbered sections
   - Verify correct section is returned for any section number
   - **Feature: confluence-jira-automation, Property 3: Section Parsing Accuracy**

4. **Property Test for Table Row Extraction** (Property 4)
   - Generate random HTML tables with varying structures
   - Verify all rows are extracted with complete metadata
   - **Feature: confluence-jira-automation, Property 4: Table Row Extraction Completeness**

5. **Property Test for Authenticated Requests** (Property 5)
   - Generate random cookie sets
   - Verify all cookies are included in subsequent requests
   - **Feature: confluence-jira-automation, Property 5: Authenticated Request Propagation**

6. **Property Test for Content Extraction** (Property 6)
   - Generate random HTML pages with navigation/headers
   - Verify extracted content excludes these elements
   - **Feature: confluence-jira-automation, Property 6: Content Extraction Cleanliness**

7. **Property Test for Retry Logic** (Property 7)
   - Generate random failure scenarios
   - Verify exactly 3 retries with exponential backoff
   - **Feature: confluence-jira-automation, Property 7: Retry Logic Consistency**

8. **Property Test for Status Normalization** (Property 8)
   - Generate random status indicators and keywords
   - Verify output is always Green, Yellow, or Red
   - **Feature: confluence-jira-automation, Property 8: Status Detection Normalization**

9. **Property Test for Summary Length** (Property 9)
   - Generate random sets of module summaries
   - Verify comprehensive summary is 3-4 sentences
   - **Feature: confluence-jira-automation, Property 9: Comprehensive Summary Length**

10. **Property Test for Red Status Highlighting** (Property 10)
    - Generate random summary sets with at least one Red status
    - Verify comprehensive summary mentions red modules
    - **Feature: confluence-jira-automation, Property 10: Red Status Highlighting**

11. **Property Test for Jira URL Parsing** (Property 11)
    - Generate random valid Jira URLs
    - Verify project key extraction returns valid format
    - **Feature: confluence-jira-automation, Property 11: Jira URL Parsing Correctness**

12. **Property Test for Issue Extraction** (Property 12)
    - Generate random Jira API responses
    - Verify all issues extracted with complete metadata
    - **Feature: confluence-jira-automation, Property 12: Jira Issue Extraction Completeness**

13. **Property Test for Issue Grouping** (Property 13)
    - Generate random lists of Jira issues
    - Verify each issue appears in exactly one status group
    - **Feature: confluence-jira-automation, Property 13: Issue Grouping Correctness**

14. **Property Test for Table Structure** (Property 14)
    - Generate random lists of Jira issues
    - Verify generated HTML has 5 columns and correct row count
    - **Feature: confluence-jira-automation, Property 14: Jira Table Structure Validity**

15. **Property Test for High-Priority Filtering** (Property 15)
    - Generate random issue lists with >50 items
    - Verify filtered result contains only high-priority and ≤50 items
    - **Feature: confluence-jira-automation, Property 15: High-Priority Filtering**

16. **Property Test for Content Preservation** (Property 16)
    - Generate random Confluence pages with multiple sections
    - Verify updates don't modify unrelated sections
    - **Feature: confluence-jira-automation, Property 16: Content Preservation**

17. **Property Test for Error Logging** (Property 17)
    - Generate random module failures
    - Verify logs contain module name and failure reason
    - **Feature: confluence-jira-automation, Property 17: Error Logging Completeness**

18. **Property Test for Processing Summary** (Property 18)
    - Generate random workflow executions with varying success/failure
    - Verify processed + failed = total attempted
    - **Feature: confluence-jira-automation, Property 18: Processing Summary Accuracy**

19. **Property Test for Backup Creation** (Property 19)
    - Generate random update failures
    - Verify backup file is created with correct content
    - **Feature: confluence-jira-automation, Property 19: Backup File Creation**

20. **Property Test for Optional Jira** (Property 20)
    - Generate random workflows with Jira skipped
    - Verify workflow completes successfully
    - **Feature: confluence-jira-automation, Property 20: Workflow Optional Jira**

### Integration Testing

Integration tests will verify end-to-end workflows:

1. **Full Workflow Test**: Test complete automation from authentication to Confluence update
2. **Jira Integration Test**: Test Jira data fetching and table generation
3. **Error Recovery Test**: Test system behavior with various failure scenarios
4. **Performance Test**: Verify 10 modules process in <5 minutes

### Testing Framework

- **Unit Tests**: `pytest` with `pytest-mock` for mocking
- **Property-Based Tests**: `hypothesis` library (minimum 100 iterations per property)
- **Integration Tests**: `pytest` with real Chrome instance and mock Confluence/Jira APIs
- **Coverage Target**: 80% code coverage minimum

## Performance Considerations

### Optimization Strategies

1. **Parallel Processing**: Process multiple modules concurrently (max 5 concurrent)
2. **Caching**: Cache authenticated cookies for session duration
3. **Connection Pooling**: Reuse HTTP connections for multiple requests
4. **Lazy Loading**: Load AI models only when needed
5. **Batch Operations**: Batch Confluence updates when possible

### Performance Targets

- **Authentication**: <30 seconds (including user interaction)
- **Module Processing**: <30 seconds per module
- **Jira Integration**: <60 seconds for typical project (<100 issues)
- **Total Workflow**: <5 minutes for 10 modules

### Resource Management

- **Memory**: Limit concurrent operations to prevent memory exhaustion
- **Network**: Implement rate limiting to respect API limits
- **Browser**: Close Chrome connection after workflow completion
- **Files**: Clean up temporary files after successful execution

## Security Considerations

### Authentication Security

- **Cookie Storage**: Store cookies in memory only, never persist to disk
- **Token Masking**: Mask authentication tokens in logs
- **Session Timeout**: Validate cookies before each request
- **Secure Communication**: Use HTTPS for all API requests

### Data Privacy

- **PII Handling**: Avoid logging user names or email addresses
- **Content Sanitization**: Sanitize HTML content before processing
- **Access Control**: Respect Confluence/Jira permissions
- **Audit Trail**: Log all page modifications with timestamps

### Input Validation

- **URL Validation**: Validate all URLs before fetching
- **HTML Sanitization**: Sanitize user-provided HTML
- **Project Key Validation**: Validate Jira project keys against allowed format
- **Size Limits**: Enforce maximum sizes for fetched content

## Deployment Considerations

### Environment Setup

1. **Python Version**: Python 3.9+
2. **Dependencies**: Install via `requirements.txt`
3. **Chrome**: Google Chrome must be installed
4. **Environment Variables**: Configure via `.env` file

### Configuration

```python
# .env file
CONFLUENCE_BASE_URL=https://confluence.atl.ring.com
PAGE_ID=2814198025
SECTION_NUMBER=8
CHROME_DEBUG_PORT=9222
AI_MODEL=claude-3-sonnet
AI_API_KEY=<your-api-key>
JIRA_BASE_URL=https://jira.amazon.com
MAX_RETRIES=3
RETRY_DELAY=2
```

### Monitoring

- **Logging**: Rotate logs daily, retain for 30 days
- **Metrics**: Track success rate, processing time, error counts
- **Alerts**: Alert on authentication failures, API errors
- **Health Checks**: Verify Chrome connection before workflow

## Future Enhancements

1. **Service Account**: Replace cookie-based auth with service account
2. **Scheduled Execution**: Add cron job support for automated runs
3. **Email Notifications**: Send completion notifications to stakeholders
4. **Manual Override Detection**: Detect and preserve manual edits
5. **Multi-Page Support**: Support multiple Confluence pages
6. **Advanced Filtering**: Add custom filters for Jira issues
7. **Dashboard**: Web dashboard for monitoring and configuration
8. **API Mode**: Expose functionality via REST API
