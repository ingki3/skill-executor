# Tasks: Separate Prompt YAML Management

**Feature**: Separate Prompt YAML Management
**Implementation Plan**: [plan.md](plan.md)
**Status**: Initialized
**Strategy**: MVP First (Setup & Loader) -> Foundational Migration (Security) -> Complete Migration (Execution) -> Polish (Reload API)

## Phase 1: Setup

- [X] T001 [P] Create centralized prompt directory in `backend/src/prompt/`
- [X] T002 [P] Install `PyYAML` dependency in `backend/pyproject.toml`
- [X] T003 [P] Initialize YAML files for namespaces: `security.yaml`, `execution.yaml`, `search.yaml`

## Phase 2: Foundational

- [X] T004 Implement `PromptLoader` utility with caching in `backend/src/core/prompt_loader.py`
- [X] T005 [P] Create unit tests and performance benchmark for `PromptLoader` in `backend/tests/unit/test_prompt_loader.py`
- [X] T006 [P] Register `PromptLoader` instance in `backend/src/core/__init__.py` or equivalent for global access

## Phase 3: User Story 1 - Centralized Prompt Management (Security)

**Goal**: Migrate security-related prompts to YAML.
**Independent Test**: Run a skill registration and verify LLM-based risk analysis still functions correctly using the loaded prompt.

- [X] T007 [US1] Externalize security scan prompt to `backend/src/prompt/security.yaml`
- [X] T008 [US1] Update `SecurityService.scan_skill` to use `PromptLoader` in `backend/src/services/security.py`
- [X] T009 [US1] Externalize metadata extraction prompt (if any) to `backend/src/prompt/registration.yaml`

## Phase 4: User Story 2 - Zero Hardcoded Prompts (Execution)

**Goal**: Complete the migration for the execution engine.
**Independent Test**: Execute a complex skill and verify the ReACT loop operates normally using templates from YAML.

- [X] T010 [US2] Externalize ReACT loop template to `backend/src/prompt/execution.yaml`
- [X] T011 [US2] Update `ExecutionService._execute_agent_loop` to use `PromptLoader` in `backend/src/services/execution.py`
- [X] T012 [US2] Externalize simple execution template to `backend/src/prompt/execution.yaml`
- [X] T013 [US2] Update `ExecutionService._execute_simple` to use `PromptLoader` in `backend/src/services/execution.py`
- [X] T014 [US2] Audit `backend/src/services/` for any remaining hardcoded LLM instructions

## Phase 5: Polish & Cross-Cutting

- [X] T015 Implement `POST /execution/prompts/reload` admin endpoint in `backend/src/api/execution_router.py`
- [X] T016 Add error logging for missing keys or malformed YAML in `PromptLoader`
- [X] T017 Update `backend/README.md` with instructions on how to manage prompts

## Dependencies

1. Foundational `PromptLoader` (Phase 2) MUST be completed before any migration tasks (Phase 3 & 4).
2. Phase 3 and Phase 4 can technically run in parallel if multiple developers are assigned.

## Implementation Strategy

1. **MVP**: Get the `PromptLoader` working and migrate ONE prompt (Security) to prove the pattern.
2. **Incremental**: Migrate Execution prompts one by one.
3. **Audit**: Use `grep` to ensure 100% externalization before marking US2 complete.
