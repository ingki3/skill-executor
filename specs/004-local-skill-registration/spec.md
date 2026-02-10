# Feature Specification: Local Skill Registration

**Feature Branch**: `004-local-skill-registration`  
**Created**: 2026-02-07  
**Status**: Draft  
**Input**: User description: "search repo에 register skill 을 추가해줘. search repo 는 디렉토리, register skill은 skill이 입력 된 폴더야."

## Clarifications

### Session 2026-02-07

- Q: Path Boundary Security → A: Restricted to project directory (paths must be within the project root)
- Q: Duplicate Resolution Strategy → A: Overwrite with confirmation (prompt user if skill already exists)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Search and List Local Skills (Priority: P1)

As an administrator, I want to search a local directory on the server so that I can see a list of subdirectories that contain potential skills for registration.

**Why this priority**: High. This is the foundation for local skill management.

**Independent Test**: Can be tested by providing a valid local path to the search functionality and verifying that all sub-folders (potential skills) are correctly listed in the UI.

**Acceptance Scenarios**:

1. **Given** a valid local directory path, **When** I initiate a search, **Then** the system displays a list of all subdirectories within that path.
2. **Given** an invalid or inaccessible local path, **When** I initiate a search, **Then** the system displays a clear error message.

---

### User Story 2 - Register Local Skill (Priority: P1)

As an administrator, I want to select a specific folder from the search results and register it as a skill so that it becomes available for execution in my agent environment.

**Why this priority**: High. This is the core action requested by the user.

**Independent Test**: Can be tested by selecting a subdirectory that contains valid skill metadata and code, and verifying it appears in the "Registered Skills" list.

**Acceptance Scenarios**:

1. **Given** a list of subdirectories from a local search, **When** I select one or more and click "Register", **Then** the system processes them through the standard registration workflow (including security scan).
2. **Given** a subdirectory without valid metadata, **When** I attempt to register it, **Then** the system flags it as a failed registration with a descriptive error.

---

### Edge Cases

- **Path Permissions**: What happens if the server process doesn't have read access to the directory? (Assumption: System shows a "Permission Denied" error).
- **Symbolic Links**: Should the system follow symlinks? (Assumption: System follows symlinks to a maximum depth of 1 to avoid circular dependencies).
- **Empty Directories**: How are subdirectories with no content handled? (Assumption: They are listed but registration will fail during the metadata discovery phase).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an interface to enter a local path for "Search Repo".
- **FR-002**: System MUST list all immediate subdirectories of the provided local path as potential "Register Skill" folders.
- **FR-003**: System MUST identify valid skills by searching for `skill.yaml` or `SKILL.md` within the selected local folders.
- **FR-004**: System MUST support the same registration workflow for local folders as it does for GitHub repositories (metadata extraction, security scan, registry addition).
- **FR-005**: System MUST validate that the provided path exists, is a directory, and is located within the project root directory.
- **FR-006**: System MUST prompt the user for confirmation before overwriting or updating an existing skill in the registry.

### Key Entities

- **Local Repository**: An absolute path on the host system containing multiple skill folders.
- **Local Skill Folder**: A subdirectory within a local repository that contains the required skill definition files.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can list skills from a local directory containing 100 subfolders in under 2 seconds.
- **SC-002**: 100% of skills successfully registered from a local folder are immediately available for execution checks.
- **SC-003**: The system successfully prevents registration of local folders that fail the mandatory automated security scan.
- **SC-004**: System correctly handles and reports at least 3 distinct error types (Path Not Found, Permission Denied, Missing Metadata).