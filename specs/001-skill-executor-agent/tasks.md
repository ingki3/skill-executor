---

description: "Task list for Skill Executor Agent implementation"
---

# Tasks: Skill Executor Agent

**Input**: Design documents from `/specs/001-skill-executor-agent/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included as standard practice for this project's quality standards.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Tests**: `backend/tests/`, `frontend/tests/` (Docker-based)
- **Docker**: `docker/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (backend/, frontend/, docker/, .skills/)
- [x] T002 Initialize backend with `uv init` and install FastAPI, gitpython, langchain, faiss-cpu
- [x] T003 Initialize frontend with `npm init` (Vite/React) and install Tailwind CSS
- [x] T004 Create Dockerfile for backend, frontend and docker-compose.yml
- [x] T005 [P] Configure linting and formatting (ruff for python, eslint/prettier for react)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup Pydantic models for Skill and ExecutionLog in backend/src/models/
- [x] T007 [P] Implement FAISS vector store initialization in backend/src/core/vector_store.py
- [x] T008 [P] Implement local JSON registry management in backend/src/services/registry.py
- [x] T009 [P] Setup LLM clients (Gemini Flash & Pro) in backend/src/core/llm_clients.py
- [x] T010 Setup base FastAPI app with CORS and error handling in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure Skill Registration (Priority: P1) 🎯 MVP

**Goal**: Register skills from GitHub with LLM-based security scanning

**Independent Test**: Register a safe repo (success) vs. malicious repo (403 Forbidden)

### Tests for User Story 1

- [x] T011 [P] [US1] Unit tests for security scan logic in backend/tests/test_security_service.py
- [x] T012 [P] [US1] Integration test for /skills/register in backend/tests/test_registration.py
(Note: Integration test placeholder created, real execution requires setup)

### Implementation for User Story 1

- [x] T013 [P] [US1] Implement GitHub cloning service using gitpython in backend/src/services/github.py
- [x] T014 [US1] Implement LLM-based security scanning service in backend/src/services/security.py
- [x] T015 [US1] Implement registration service (Clone -> Scan -> Index -> Register) with support for batch directory scanning in backend/src/services/registration.py
- [x] T016 [US1] Implement POST /skills/register endpoint supporting both single URL and batch folder paths in backend/src/api/registration_router.py
- [x] T017 [US1] Add manual "Sync" logic (re-pull and re-scan) in backend/src/services/registration.py
- [x] T018 [US1] Implement POST /skills/{id}/sync endpoint in backend/src/api/registration_router.py

**Checkpoint**: User Story 1 (MVP) fully functional and testable independently

---

## Phase 4: User Story 2 - Intelligent Skill Execution (Priority: P2)

**Goal**: Semantic search and routed execution (Direct vs ReACT)

**Independent Test**: Query "Simple" skill (direct response) vs "Complex" skill (multi-step log)

### Tests for User Story 2

- [x] T019 [P] [US2] Unit tests for semantic search and confidence thresholding in backend/tests/test_search.py
- [x] T020 [P] [US2] Integration test for /skills/execute in backend/tests/test_execution.py

### Implementation for User Story 2

- [x] T021 [P] [US2] Implement semantic search service with confidence threshold in backend/src/services/search.py
- [x] T022 [US2] Implement "Simple" execution path (Gemini Flash) in backend/src/services/execution.py
- [x] T023 [US2] Implement "Complex" execution path (Gemini Pro ReACT) with a maximum 10-step reasoning limit in backend/src/services/execution.py
- [x] T024 [US2] Implement execution router with "No Match Found" fallback in backend/src/services/router.py
- [x] T025 [US2] Implement POST /skills/execute endpoint in backend/src/api/execution_router.py
- [x] T026 [US2] Implement execution logging to local JSON in backend/src/services/logger.py

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Skill Management Dashboard (Priority: P3)

**Goal**: Admin UI for visibility and manual operations

**Independent Test**: View registered skill list, trigger sync, and see health status

### Implementation for User Story 3

- [x] T027 [P] [US3] Create frontend API client in frontend/src/services/api.ts
- [x] T028 [P] [US3] Create SkillCard and SyncButton components in frontend/src/components/
- [x] T029 [US3] Implement Skill List page in frontend/src/pages/Dashboard.tsx
- [x] T030 [US3] Implement Skill Details page with execution logs in frontend/src/pages/SkillDetails.tsx
- [x] T031 [US3] Implement Registration form supporting both Single and Batch modes in frontend/src/pages/Register.tsx
- [x] T032 [US3] Implement GET /skills endpoint in backend/src/api/registration_router.py
- [x] T033 [US3] Implement GET /health endpoint in backend/src/api/main.py

**Checkpoint**: All user stories functional with full UI visibility

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T034 [P] Update README.md and quickstart.md with final API details
- [ ] T035 Code cleanup and dependency optimization
- [ ] T036 Final Docker image hardening
- [ ] T037 [P] Add unit tests for edge cases (malformed metadata, timeout) in backend/tests/
- [ ] T038 Verify all success criteria (SC-001 to SC-005)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Phase 1
- **User Stories (Phase 3+)**: All depend on Phase 2 completion
  - US1 is the MVP and should be completed first
  - US2 and US3 can proceed in parallel once US1 foundations are in place

### User Story Dependencies

- **US1 (P1)**: Independent after Phase 2
- **US2 (P2)**: Requires US1 to have skills to execute
- **US3 (P3)**: Requires US1/US2 endpoints to show data

---

## Parallel Example: Foundational Phase

```bash
# Work on these concurrently as they touch different files:
Task: "Implement FAISS vector store initialization in backend/src/core/vector_store.py"
Task: "Implement local JSON registry management in backend/src/services/registry.py"
Task: "Setup LLM clients (Gemini Flash & Pro) in backend/src/core/llm_clients.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2
2. Complete Phase 3 (US1)
3. Validate: Register a safe skill and verify it exists in `.skills/`

### Incremental Delivery

1. Add US2: Enable execution of the registered skills.
2. Add US3: Provide the UI for easier management.

---

## Notes

- All backend implementation MUST use `uv` for package management.
- All frontend implementation MUST use `npm` and Tailwind CSS.
- Verification MUST be performed inside Docker containers.
