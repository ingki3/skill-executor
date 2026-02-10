# Tasks: Unified Docker Image and Skill Testing

**Input**: Design documents from `/specs/002-unified-docker-image/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are generated for each user story to ensure independent verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Tests**: `backend/tests/`, `frontend/tests/`
- **Docker**: Root directory `Dockerfile`, `docker-compose.yml`, `scripts/entrypoint.sh`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization for unified build

- [X] T001 Create unified multi-stage `Dockerfile` in root directory
- [X] T002 Update `docker-compose.yml` to use the unified image and define volumes for `.skills/` and `.skill-executor-data/`
- [X] T003 Create `scripts/entrypoint.sh` to manage both frontend and backend processes
- [X] T004 [P] Update `backend/pyproject.toml` with `httpx` for GitHub API calls
- [X] T005 [P] Configure frontend environment variables in `frontend/.env` to point to the backend port (8000)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for multi-service execution and persistent storage

**⚠️ CRITICAL**: Foundation must be verified before user story implementation

- [X] T006 Implement volume mount verification in `backend/src/services/registry.py`
- [X] T007 [P] Implement automated risk analysis (PII, malicious code, system ops) in `backend/src/services/security.py`
- [X] T008 [P] Create API router for registration in `backend/src/api/registration_router.py`
- [X] T009 [P] Setup base frontend service for registration in `frontend/src/services/registration_api.ts`
- [X] T010 Verify `scripts/entrypoint.sh` correctly forwards signals and manages logs for both services

**Checkpoint**: Foundation ready - Docker environment supports persistent skills and multi-port access.

---

## Phase 3: User Story 1 - Single Image Deployment (Priority: P1) 🎯 MVP

**Goal**: Build and run both UI and API from a single image with separate ports.

**Independent Test**: Build image, run with volumes, and verify UI (3000) and API (8000) are accessible.

### Tests for User Story 1

- [X] T011 [P] [US1] Integration test for multi-service availability in `backend/tests/test_unified_deployment.py`

### Implementation for User Story 1

- [X] T012 [US1] Refine `Dockerfile` multi-stage build to optimize frontend asset size and backend environment
- [X] T013 [US1] Implement process monitoring in `scripts/entrypoint.sh` (e.g., exit if either service fails)
- [X] T014 [US1] Configure `backend/src/main.py` to allow CORS from the frontend port
- [X] T015 [US1] Update `frontend/src/services/api.ts` to use the configured API port at runtime

**Checkpoint**: User Story 1 complete - Application is now a single-image deployment.

---

## Phase 4: User Story 2 - Bulk Skill Registration (Priority: P1)

**Goal**: Select 3-4 skills from a GitHub repo via UI and register them locally.

**Independent Test**: Input repo URL, select specific skills from list, and confirm they appear in the local registry.

### Tests for User Story 2

- [X] T016 [P] [US2] Contract test for `/api/registration/list-skills` in `backend/tests/contract/test_listing.py`
- [X] T017 [P] [US2] Integration test for selective registration in `backend/tests/integration/test_bulk_registration.py`

### Implementation for User Story 2

- [X] T018 [US2] Implement `list_repository_skills` in `backend/src/services/github.py` using GitHub API
- [X] T019 [US2] Implement `/api/registration/list-skills` with timeout handling in `backend/src/api/registration_router.py`
- [X] T020 [US2] Update `register_github_skill` in `backend/src/services/registration.py` to handle multiple selected paths
- [X] T021 [US2] Create `SkillSelectionList` component in `frontend/src/components/SkillSelectionList.tsx`
- [X] T022 [US2] Update registration page in `frontend/src/pages/Dashboard.tsx` with loading states for skill listing
- [X] T023 [US2] Ensure registered skills are persisted to the `.skills/` volume mount

**Checkpoint**: User Story 2 complete - Users can now bulk-register specific skills from community repositories.

---

## Phase 5: User Story 3 - Verified Skill Execution (Priority: P2)

**Goal**: Execute registered skills within the unified container and verify results.

**Independent Test**: Trigger execution for each of the 4 test skills and confirm successful response status.

### Tests for User Story 3

- [X] T024 [P] [US3] Integration test for execution of volume-persisted skills in `backend/tests/integration/test_unified_execution.py`

### Implementation for User Story 3

- [X] T025 [US3] Verify execution environment in `backend/src/services/execution.py` correctly locates skills in the mounted volume
- [X] T026 [US3] Add execution status indicators to the dashboard in `frontend/src/components/SkillCard.tsx`
- [X] T027 [US3] Implement execution verification loop to test 3-4 registered skills from `awesome-claude-skills`

**Checkpoint**: User Story 3 complete - The entire skill lifecycle is validated in the unified image.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and optimization

- [X] T028 [P] Update `README.md` with the new single-image build and run instructions
- [X] T029 [P] Optimize `Dockerfile` cache layers for faster builds
- [X] T030 Clean up temporary skill data in `.skill-executor-data/`
- [X] T031 Run full validation of `specs/002-unified-docker-image/quickstart.md`
- [X] T032 Verify SC-004: Measure and document container initialization time (Target < 15s)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 (volume paths and port structure).
- **User Stories (Phase 3-5)**: Depend on Foundational completion.
  - US1 (Deployment) is the top priority as it enables testing of other stories.
  - US2 (Registration) and US3 (Execution) are sequential.

### User Story Dependencies

- **US1**: Must be complete to verify US2 and US3 in the target environment.
- **US2**: Must be complete to provide the 3-4 skills needed for US3.
- **US3**: Final validation.

---

## Implementation Strategy

### MVP First (Single Image + 1 Skill)

1. Complete Phase 1 and 2.
2. Complete US1 (Single Image Deployment).
3. Register a single skill manually to verify the volume and execution path.

### Incremental Delivery

1. Foundation + US1 → "Single Image MVP".
2. Add US2 → "Bulk Community Registration".
3. Add US3 → "Full Lifecycle Validation".

---

## Notes

- [P] tasks can run in parallel within their phase.
- Volume mounts `$(pwd)/.skills` and `$(pwd)/.skill-executor-data` are critical for persistence across `docker run` commands.
- The `entrypoint.sh` script is the "glue" for the unified container.
