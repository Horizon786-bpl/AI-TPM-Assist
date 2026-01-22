# Requirements Document

## Introduction

This document specifies the requirements for an automated system that reads Confluence pages with Midway authentication, summarizes linked documents, and integrates Jira project data into a Confluence table. The system is designed for TPMs at Ring who need to compile weekly status updates from multiple sources.

## Glossary

- **Confluence**: Amazon's internal wiki and documentation platform
- **Midway**: Amazon's authentication system with Posture cookies
- **Flan Page**: The main Confluence page containing the "Functional Status Update" table
- **Module**: A functional area tracked in the status table (e.g., Hardware, Compliance)
- **Module Link**: A URL in the table pointing to a detailed update page for that module
- **Jira**: Amazon's issue tracking system
- **Status Indicator**: A color-coded status (Green/Yellow/Red) showing module health
- **Comprehensive Summary**: An executive-level overview across all modules
- **Chrome Remote Debugging**: A Chrome feature allowing programmatic browser control

## Requirements

### Requirement 1: Midway Authentication and Document Access

**User Story:** As a TPM, I want the system to automatically authenticate with Midway and access Confluence pages, so that I don't need to manually export cookies or handle authentication.

#### Acceptance Criteria

1. WHEN the system starts THEN the Automation System SHALL connect to Chrome with remote debugging enabled
2. WHEN Chrome is not running with debugging THEN the Automation System SHALL launch Chrome with the remote debugging port configured
3. WHEN the user is not authenticated THEN the Automation System SHALL navigate to the Confluence page and wait for user authentication
4. WHEN the user completes Midway authentication THEN the Automation System SHALL detect authentication completion and extract session cookies
5. WHEN cookies are extracted THEN the Automation System SHALL store cookies for subsequent requests during the session

### Requirement 2: Confluence Page Parsing

**User Story:** As a TPM, I want the system to read the Functional Status Update table from the Flan page, so that it knows which modules to process.

#### Acceptance Criteria

1. WHEN the Flan page is accessed THEN the Automation System SHALL locate the "Functional Status Update" section by section number
2. WHEN the section is found THEN the Automation System SHALL parse the table structure and extract all rows
3. WHEN parsing table rows THEN the Automation System SHALL extract the Module name, Link URL, current Status, and Owner for each row
4. WHEN a row contains an empty Link column THEN the Automation System SHALL skip that row and continue processing
5. WHEN parsing completes THEN the Automation System SHALL return a list of modules with their metadata

### Requirement 3: Module Link Processing and Summarization

**User Story:** As a TPM, I want the system to open each module's linked page and generate a summary, so that I have condensed updates for all modules.

#### Acceptance Criteria

1. WHEN processing a module THEN the Automation System SHALL fetch the content from the module's Link URL using authenticated cookies
2. WHEN the linked page is fetched THEN the Automation System SHALL extract the main content excluding navigation and headers
3. WHEN content is extracted THEN the Automation System SHALL send the content to an AI service for summarization
4. WHEN generating a summary THEN the Automation System SHALL produce a professional paragraph capturing key updates, achievements, and blockers
5. WHEN a module link fails to load THEN the Automation System SHALL retry up to 3 times with exponential backoff before marking as failed

### Requirement 4: Status Extraction

**User Story:** As a TPM, I want the system to extract the status indicator from each module page, so that I can quickly identify at-risk modules.

#### Acceptance Criteria

1. WHEN processing a module page THEN the Automation System SHALL search for a "Status" section in the content
2. WHEN a Status section is found THEN the Automation System SHALL identify the color indicator (Green, Yellow, or Red)
3. WHEN no explicit status is found THEN the Automation System SHALL analyze content for status keywords to infer the status
4. WHEN status is determined THEN the Automation System SHALL map it to the standard color codes (Green/Yellow/Red)
5. WHEN status cannot be determined THEN the Automation System SHALL default to Yellow and log a warning

### Requirement 5: Comprehensive Summary Generation

**User Story:** As a TPM, I want the system to generate an overall summary across all modules, so that leadership can get a quick executive overview.

#### Acceptance Criteria

1. WHEN all module summaries are generated THEN the Automation System SHALL analyze all summaries to identify common themes
2. WHEN analyzing summaries THEN the Automation System SHALL identify critical blockers and key achievements
3. WHEN generating the comprehensive summary THEN the Automation System SHALL produce 3-4 sentences providing an executive-level overview
4. WHEN Red status modules exist THEN the Automation System SHALL highlight them in the comprehensive summary
5. WHEN all modules are Green THEN the Automation System SHALL state that all modules are on track

### Requirement 6: Jira Integration - Project Selection

**User Story:** As a TPM, I want to specify which Jira project to integrate, so that the system can fetch relevant issue data.

#### Acceptance Criteria

1. WHEN summaries are generated THEN the Automation System SHALL prompt the user to provide a Jira project name or link
2. WHEN the user provides a Jira link THEN the Automation System SHALL extract the project key from the URL
3. WHEN the user provides a project name THEN the Automation System SHALL validate the project exists in Jira
4. WHEN the project is invalid THEN the Automation System SHALL display an error and re-prompt the user
5. WHEN the user skips Jira integration THEN the Automation System SHALL proceed without Jira data

### Requirement 7: Jira Data Extraction

**User Story:** As a TPM, I want the system to fetch issue data from the specified Jira project, so that I can include project status in my Confluence page.

#### Acceptance Criteria

1. WHEN a valid Jira project is provided THEN the Automation System SHALL authenticate with Jira using the same Midway cookies
2. WHEN authenticated THEN the Automation System SHALL query for all issues in the project
3. WHEN fetching issues THEN the Automation System SHALL extract issue key, summary, status, assignee, and priority for each issue
4. WHEN issues are fetched THEN the Automation System SHALL group issues by status (To Do, In Progress, Done, etc.)
5. WHEN Jira API rate limits are encountered THEN the Automation System SHALL implement exponential backoff and retry

### Requirement 8: Jira Table Generation in Confluence

**User Story:** As a TPM, I want the system to create a Jira status table in the Confluence page, so that stakeholders can see project progress.

#### Acceptance Criteria

1. WHEN Jira data is fetched THEN the Automation System SHALL locate or create a "Jira Status" section in the Confluence page
2. WHEN creating the table THEN the Automation System SHALL include columns for Issue Key, Summary, Status, Assignee, and Priority
3. WHEN populating the table THEN the Automation System SHALL add one row per issue with all extracted data
4. WHEN the table exceeds 50 issues THEN the Automation System SHALL include only high-priority issues and provide a link to full results
5. WHEN updating the page THEN the Automation System SHALL preserve existing content outside the Jira Status section

### Requirement 9: Confluence Page Update

**User Story:** As a TPM, I want the system to update the Confluence page with all generated content, so that the page reflects current status.

#### Acceptance Criteria

1. WHEN all content is generated THEN the Automation System SHALL display a preview of changes to the user
2. WHEN the user confirms THEN the Automation System SHALL update the Comments column for each module with the generated summary
3. WHEN updating THEN the Automation System SHALL update the Status column with the extracted status color
4. WHEN updating THEN the Automation System SHALL update the Comprehensive Summary row with the overall summary
5. WHEN Jira integration is used THEN the Automation System SHALL create or update the Jira Status section with the generated table

### Requirement 10: Error Handling and Reporting

**User Story:** As a TPM, I want clear error messages when something fails, so that I can troubleshoot issues quickly.

#### Acceptance Criteria

1. WHEN a module fails to process THEN the Automation System SHALL log the error with module name and failure reason
2. WHEN processing completes THEN the Automation System SHALL display a summary showing successful and failed modules
3. WHEN authentication fails THEN the Automation System SHALL provide clear instructions for re-authentication
4. WHEN network errors occur THEN the Automation System SHALL retry with exponential backoff before failing
5. WHEN the final update fails THEN the Automation System SHALL save the generated content to a local HTML file as backup
