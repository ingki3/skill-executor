# Feature Specification: Separate Prompt YAML Management

**Feature Branch**: `010-separate-prompt-yaml`  
**Created**: 2026-02-08  
**Status**: Draft  
**Input**: User description: "'/Users/hyungjoolee/dev/skill-executor/backend/src' 아래 prompt 폴더를 만들고, 현재 코드 상에 사용되고 있는 prompt를 yaml 파일 형태로 분리해서 관리하도록 해줘."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Centralized Prompt Management (Priority: P1)

As a developer, I want to manage all LLM prompts in dedicated YAML files rather than hardcoding them in Python code, so that prompts are easier to read, version control, and update independently of logic.

**Why this priority**: This is the core request. It improves maintainability and separation of concerns between code logic and prompt engineering.

**Independent Test**: Can be fully tested by creating a YAML file in the new prompt directory and verifying that the backend can retrieve and use the content of that file for an LLM task.

**Acceptance Scenarios**:

1. **Given** a prompt template defined in `backend/src/prompt/example.yaml`, **When** the backend service requests the "example" prompt, **Then** it should receive the exact string content from the YAML file.
2. **Given** a prompt template with placeholders (e.g., `{query}`), **When** the backend loads and formats this prompt, **Then** the placeholders should be correctly replaced with dynamic data.

---

### User Story 2 - Zero Hardcoded Prompts (Priority: P2)

As a system administrator, I want to ensure that no LLM prompts are buried in the source code, so that I can audit and refine agent behavior without searching through logic files.

**Why this priority**: Ensures complete migration and prevents "leakage" of prompts back into code.

**Independent Test**: Perform a global search for known prompt keywords in `.py` files and verify that only the loading mechanism remains, not the prompt text itself.

**Acceptance Scenarios**:

1. **Given** the migration is complete, **When** searching for major prompt strings in `backend/src/services/`, **Then** no matches should be found except for references to YAML keys.

---

### Edge Cases

- **Missing YAML file**: How does the system handle a request for a prompt key that doesn't exist? (Should fail gracefully with a descriptive error).
- **Malformed YAML**: What happens if a prompt file has syntax errors? (Should log an error and fallback to a default or crash early during initialization).
- **Duplicate Keys**: What happens if multiple files define the same prompt key? (Should prioritize a specific directory or merge based on a defined hierarchy).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST have a dedicated directory at `backend/src/prompt/` for storing prompt definitions.
- **FR-002**: System MUST migrate all existing hardcoded prompts from the backend codebase into YAML files within this directory.
- **FR-003**: System MUST implement a prompt loader utility that can fetch templates by file name or key.
- **FR-004**: System MUST support standard string formatting placeholders (e.g., `.format()` or `f-string` style) within the externalized prompts.
- **FR-005**: System MUST validate that all moved prompts are correctly formatted YAML.

### Key Entities *(include if feature involves data)*

- **Prompt Template**: An externalized string containing instructions for an LLM, possibly including placeholders for dynamic injection.
- **Prompt Loader**: A service or utility responsible for reading, caching (optional), and returning prompt strings from the filesystem.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of LLM prompts previously hardcoded in the backend are externalized to YAML.
- **SC-002**: The backend successfully executes all core functions (registration, execution, risk review) using prompts loaded from YAML files.
- **SC-003**: All existing backend integration tests pass, ensuring no functional regressions after migration.
- **SC-004**: Adding or updating a prompt requires only editing a YAML file, not Python code.