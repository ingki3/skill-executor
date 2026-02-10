# Tasks: Local Skill Registration

**Input**: Design documents from `/specs/004-local-skill-registration/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and base configuration

- [X] T001 Initialize `LocalFSService` placeholder in `backend/src/services/local_fs.py`
- [X] T002 Update `backend/src/services/registration.py` to support non-GitHub sources (bypass cloning)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core logic for path validation and directory traversal

- [X] T003 Implement `validate_path_boundary` in `backend/src/services/local_fs.py` (restricted to project root)
- [X] T004 Implement `list_local_subdirectories` with metadata check in `backend/src/services/local_fs.py`
- [X] T005 [P] Implement `GET /api/skills/list-from-local` in `backend/src/api/registration_router.py`
- [X] T006 [P] Update `registration_api.ts` with local search method in `frontend/src/services/registration_api.ts`

**Checkpoint**: Foundation ready - local directory discovery is functional.

---

## Phase 3: User Story 1 - Search and List Local Skills (Priority: P1) 🎯 MVP

**Goal**: Interface to search local paths and display potential skill folders.

**Independent Test**: Use the dashboard to search a local path within the project root and verify folders are listed with correct metadata status.

### Tests for User Story 1

- [X] T007 [P] [US1] Unit test for path validation and listing in `backend/tests/test_local_fs.py`
- [X] T008 [P] [US1] Contract test for `/api/skills/list-from-local` in `backend/tests/contract/test_local_api.py`

### Implementation for User Story 1

- [X] T009 [US1] Add "Search Local" mode to registration UI in `frontend/src/pages/Dashboard.tsx`
- [X] T010 [US1] Implement path input and search trigger for local paths in `frontend/src/pages/Dashboard.tsx`
- [X] T011 [US1] Implement UI error states for SC-004: Path Not Found, Permission Denied, and Missing Metadata

**Checkpoint**: User Story 1 complete - Local folder discovery is fully available in the UI.

---

## Phase 4: User Story 2 - Register Local Skill (Priority: P1)

**Goal**: Register selected local folders as skills with security verification.

**Independent Test**: Select a local folder, trigger "Scan Selected", and verify it goes through the queue and appears in the registry.

### Tests for User Story 2

- [X] T012 [P] [US2] Integration test for local folder registration workflow in `backend/tests/integration/test_local_registration.py`

### Implementation for User Story 2

- [X] T013 [US2] Update `start_batch_scan` to handle local source paths in `backend/src/services/registration.py`
- [X] T014 [US2] Update `_run_batch_scan` to bypass cloning for local paths in `backend/src/services/registration.py`
- [X] T015 [US2] Implement duplicate skill check with metadata matching in `backend/src/services/registration.py`
- [X] T016 [US2] Add duplicate confirmation dialog to the dashboard in `frontend/src/pages/Dashboard.tsx`
- [X] T017 [US2] Ensure local skill source URL correctly points to the absolute path in the registry

**Checkpoint**: User Story 2 complete - Local skills can now be fully registered and used.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and UX refinement

- [X] T018 Update `quickstart.md` with verified Docker path examples in `specs/004-local-skill-registration/quickstart.md`
- [X] T019 Add help tooltips for "Absolute path" usage in the UI in `frontend/src/pages/Dashboard.tsx`
- [X] T020 Verify SC-001: Measure directory listing performance (Target: < 2s for 100 subfolders)
- [X] T021 Run full lifecycle validation for a local folder registration
