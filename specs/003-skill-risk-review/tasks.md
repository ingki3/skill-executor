# Tasks: Skill Risk Review

**Input**: Design documents from `/specs/003-skill-risk-review/`
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

**Purpose**: Project initialization and directory structure

- [X] T001 Create storage directory `.pending_registrations/` in `backend/`
- [X] T002 Add `.pending_registrations/` to `.gitignore` and `.dockerignore`
- [X] T003 [P] Configure environment variables for asynchronous scan timeout settings in `backend/.env`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models and persistence services

- [X] T004 Create `RegistrationBatch`, `RegistrationQueueItem`, and `RiskFinding` Pydantic models in `backend/src/models/registration.py`
- [X] T005 Implement `BatchStoreService` for persistent JSON-based batch registry in `backend/src/services/batch_store.py`
- [X] T006 [P] Update `SecurityService.analyze_risk` to return structured `RiskFinding` objects in `backend/src/services/security.py`
- [X] T007 [P] Initialize base API routes for batches in `backend/src/api/registration_router.py`

**Checkpoint**: Foundation ready - state management for pending registrations is functional.

---

## Phase 3: User Story 1 - Review Flagged Skills (Priority: P1) 🎯 MVP

**Goal**: Asynchronous scanning and UI for reviewing risky findings with code preview.

**Independent Test**: Trigger a bulk scan, poll for completion, and verify that the side-panel displays correct risk details and source code.

### Tests for User Story 1

- [X] T008 [P] [US1] Unit test for async batch scanning logic in `backend/tests/test_batch_scanning.py`
- [X] T009 [P] [US1] Contract test for batch status polling in `backend/tests/contract/test_batch_api.py`

### Implementation for User Story 1

- [X] T010 [US1] Implement async `start_batch_scan` logic in `backend/src/services/registration.py` (depends on T005, T006)
- [X] T011 [US1] Implement `GET /api/skills/registration-batches/{id}` endpoint in `backend/src/api/registration_router.py`
- [X] T012 [P] [US1] Update `registration_api.ts` with batch scanning and status polling calls in `frontend/src/services/registration_api.ts`
- [X] T013 [US1] Create `RegistrationQueue` component to list pending items in `frontend/src/components/RegistrationQueue.tsx`
- [X] T014 [US1] Create `RiskDetailsPanel` side-drawer with code and metadata (skill.yaml) preview in `frontend/src/components/RiskDetailsPanel.tsx`
- [X] T015 [US1] Integrate `RegistrationQueue` into the main `Dashboard.tsx`

**Checkpoint**: User Story 1 complete - Administrators can initiate scans and review detailed findings.

---

## Phase 4: User Story 2 - Skill Judgment Action (Priority: P1)

**Goal**: Explicitly approve or reject skills, moving approved items to the permanent registry.

**Independent Test**: Click "Approve" on a risky item and verify it appears in the active skill list; click "Reject" and verify it is removed from the queue.

### Tests for User Story 2

- [X] T016 [P] [US2] Integration test for skill approval workflow in `backend/tests/integration/test_judgment_workflow.py`

### Implementation for User Story 2

- [X] T017 [US2] Implement `POST /api/skills/registration-batches/{id}/judge` endpoint in `backend/src/api/registration_router.py`
- [X] T018 [US2] Implement judgment processing logic (approval → registry move, rejection → cleanup) in `backend/src/services/registration.py`
- [X] T019 [US2] Add judgment action buttons (Approve/Reject) to `RegistrationQueue.tsx`
- [X] T020 [US2] Add judgment actions to `RiskDetailsPanel.tsx` for quick resolution during review

**Checkpoint**: User Story 2 complete - The registration gate is fully functional.

---

## Phase 5: User Story 3 - Bulk Decision Support (Priority: P2)

**Goal**: Efficiently register all "Safe" skills with a single action.

**Independent Test**: Click "Approve All Safe" and verify all items marked `SAFE` are registered while `RISKY` items remain.

### Implementation for User Story 3

- [X] T021 [US3] Implement `POST /api/skills/registration-batches/{id}/approve-all-safe` endpoint in `backend/src/api/registration_router.py`
- [X] T022 [US3] Implement bulk approval logic in `backend/src/services/registration.py`
- [X] T023 [US3] Add "Approve All Safe" button to the `RegistrationQueue.tsx` header

**Checkpoint**: User Story 3 complete - Bulk operations are optimized for efficiency.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: UI/UX refinements and final validation

- [X] T024 [P] Add syntax highlighting to code preview using `react-syntax-highlighter` in `frontend/src/components/RiskDetailsPanel.tsx`
- [X] T025 [P] Add success/error notifications (Snackbars) for judgment actions in `frontend/src/pages/Dashboard.tsx`
- [X] T026 Implement cleanup logic for `COMPLETED` batches (delete physical code in `.pending_registrations/`) in `backend/src/services/batch_store.py`
- [X] T027 Run full validation of `specs/003-skill-risk-review/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)** & **Foundational (Phase 2)**: MUST be completed first.
- **US1 (Phase 3)**: Core functionality for the review workflow.
- **US2 (Phase 4)**: Depends on US1 (requires a queue to judge).
- **US3 (Phase 5)**: Depends on US2 (uses same judgment logic).
- **Polish (Phase 6)**: Can run in parallel with US3 or after.

### Parallel Opportunities

- T003 (Env) and T001 (Storage)
- T006 (Security findings) and T005 (Batch store)
- T008 (Unit tests) and T012 (API client)
- T024 (Syntax highlighting) and T025 (Notifications)

---

## Implementation Strategy

### MVP First (US1 + US2)

1. Complete Setup and Foundation.
2. Implement async scanning and status polling (US1).
3. Implement basic Approve/Reject actions (US2).
4. **VALIDATE**: Verify a full cycle from scan to registry addition.

### Incremental Delivery

1. Foundation ready.
2. Add detailed review panels (US1).
3. Add bulk safety approval (US3).
4. Polish UI and error handling.
