# Tasks: GitHub Direct Skill Folder Input

**Input**: Design documents from `/specs/005-github-folder-input/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Define the data structures for deep link parsing

- [X] T001 Initialize `GitHubDeepLink` Pydantic model in `backend/src/models/registration.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core parsing logic and API endpoints

- [X] T002 Implement regex-based GitHub URL parser in `backend/src/services/github.py`
- [X] T003 [P] Add `GET /api/skills/parse-github-url` endpoint in `backend/src/api/registration_router.py`
- [X] T004 Update `RegistrationService` to handle `sub_path` and `branch` parameters in `backend/src/services/registration.py`

**Checkpoint**: Foundation ready - the backend can now programmatically identify and handle deep links.

---

## Phase 3: User Story 1 - Direct Registration via Skill Folder Link (Priority: P1) 🎯 MVP

**Goal**: Enable registration from a deep link by pasting it into the dashboard.

**Independent Test**: Paste a tree/branch URL into the search field and verify the skill is added to the queue without bulk searching.

### Tests for User Story 1

- [ ] T005 [P] [US1] Unit test for URL parser logic (tree/blob/root variants) in `backend/tests/test_github_parser.py`
- [ ] T006 [P] [US1] Contract test for `/api/skills/parse-github-url` in `backend/tests/contract/test_url_api.py`

### Implementation for User Story 1

- [X] T007 [US1] Integrate deep-link detection into `register_from_url` workflow in `backend/src/services/registration.py`
- [X] T008 [P] [US1] Update `registration_api.ts` with `parseGithubUrl` method in `frontend/src/services/registration_api.ts`
- [X] T009 [US1] Update `Dashboard.tsx` to handle direct registration response from deep links

**Checkpoint**: User Story 1 complete - Direct folder links now trigger registration.

---

## Phase 4: User Story 2 - Intelligent Input Parsing (Priority: P2)

**Goal**: Automatically switch registration modes based on input URL type.

**Independent Test**: Verify the "Search" button dynamically changes behavior (or label) when a deep link is pasted.

### Implementation for User Story 2

- [X] T010 [US2] Implement auto-detection logic on URL input change in `frontend/src/pages/Dashboard.tsx`
- [X] T011 [US2] Implement auto-scan trigger for detected deep links in `frontend/src/pages/Dashboard.tsx`
- [X] T012 [US2] Add duplicate confirmation logic specifically for deep-link registrations in `frontend/src/pages/Dashboard.tsx`

**Checkpoint**: User Story 2 complete - The registration workflow is now "smart" and context-aware.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: UX refinement and validation

- [X] T013 [P] Add validation feedback for invalid deep links (e.g., path not found) in `frontend/src/pages/Dashboard.tsx`
- [X] T014 Run full lifecycle validation for a deep-link registration and verify SC-003 (Status under 15s)
- [X] T015 Ensure `blob` links (files) correctly resolve to their parent folders in `backend/src/services/github.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1 models.
- **US1 (Phase 3)**: Depends on Phase 2 logic.
- **US2 (Phase 4)**: Depends on US1 completion.
- **Polish (Phase 5)**: Final cleanup.

### Parallel Opportunities

- T003 (Backend Route) and T008 (Frontend API)
- T005 (Tests) and T007 (Implementation)
- T013 (UI Feedback) and T015 (Blob resolution)

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Setup and Foundational parsing.
2. Enable the backend to process deep links.
3. Allow the frontend to submit deep links and handle the direct registration.

### Incremental Delivery

1. Foundation ready.
2. Direct registration functional (US1).
3. "Smart" mode switching and auto-triggering (US2).
4. Full validation and edge case handling (Polish).
