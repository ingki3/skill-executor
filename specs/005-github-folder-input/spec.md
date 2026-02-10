# Feature Specification: GitHub Direct Skill Folder Input

**Feature Branch**: `005-github-folder-input`  
**Created**: 2026-02-07  
**Status**: Draft  
**Input**: User description: "github 입력할 때, skill 폴더를 바로 입력하도록 수정해줘"

## Clarifications

### Session 2026-02-07

- Q: Duplicate Registration Strategy → A: Prompt (Alert user and ask to overwrite if skill already exists)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Direct Registration via Skill Folder Link (Priority: P1)

As an administrator, I want to paste a direct link to a GitHub skill folder into the registration input, so that I can register a specific skill immediately without searching through the entire repository.

**Why this priority**: High. This simplifies the user workflow for known skills and meets the core user request.

**Independent Test**: Provide a GitHub URL pointing to a specific subdirectory (e.g., `https://github.com/ComposioHQ/awesome-claude-skills/tree/main/freshdesk-automation`) and verify that the system correctly identifies and registers only that specific skill.

**Acceptance Scenarios**:

1. **Given** a valid GitHub folder link, **When** I submit it for registration, **Then** the system parses the repository, branch, and sub-path, and adds the skill to the registration queue.
2. **Given** a link to a file within a skill folder, **When** I submit it, **Then** the system identifies the parent folder as the skill directory and proceeds with registration.

---

### User Story 2 - Intelligent Input Parsing (Priority: P2)

As an administrator, I want the registration input to intelligently differentiate between a root repository URL and a specific skill folder URL, so that the appropriate workflow (search vs. direct registration) is triggered automatically.

**Why this priority**: Medium. Improves the versatility of the registration interface.

**Independent Test**: Test with both `https://github.com/owner/repo` (should trigger search) and `https://github.com/owner/repo/tree/main/path/to/skill` (should trigger direct registration).

**Acceptance Scenarios**:

1. **Given** a root GitHub repository URL, **When** I click search, **Then** the system lists all available skills in that repository.
2. **Given** a deep link to a specific GitHub folder, **When** I submit it, **Then** the system skips the listing step and initiates the security scan for that specific folder.

---

### Edge Cases

- **Private Repositories**: How are deep links handled for private repos? (Assumption: System returns a "Repository not found or inaccessible" error if no credentials provided).
- **Invalid Paths**: What happens if the link points to a non-existent folder? (Assumption: System displays a "Path not found in repository" error).
- **Branch Specification**: How are different branch formats (e.g. `tree/master`, `tree/develop`) handled? (Assumption: System supports standard GitHub `tree/{branch}` path parsing).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support GitHub deep links (URLs containing a subdirectory path).
- **FR-002**: System MUST automatically extract the repository URL, branch name, and skill sub-path from a provided GitHub deep link (supporting both `tree` and `blob` URL variants).
- **FR-003**: System MUST allow direct registration of a single skill from a deep link, bypassing the "List Skills" step.
- **FR-004**: System MUST perform the standard security scan and judgment process for skills registered via deep links.
- **FR-005**: System MUST provide clear error feedback if a deep link path is invalid or lacks necessary metadata (`skill.yaml` or `SKILL.md`).
- **FR-006**: System MUST detect if a deep-linked skill is already registered and prompt the user for confirmation before overwriting or updating it.

### Key Entities

- **GitHub Deep Link**: A URL pointing to a specific subdirectory within a GitHub repository.
- **Registration Queue Item**: The intermediate state of the skill during the security review.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can initiate registration from a deep link in a single action (submit URL).
- **SC-002**: 100% of standard GitHub subdirectory URLs (e.g. `.../tree/branch/path`) are correctly parsed by the backend.
- **SC-003**: System provides a "Review Required" status for a deep-linked skill in under 15 seconds after submission.