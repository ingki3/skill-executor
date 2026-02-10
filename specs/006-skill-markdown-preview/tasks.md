# Tasks: Skill Markdown Preview

**Input**: Design documents from `/specs/006-skill-markdown-preview/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and library installation

- [x] T001 Install `react-markdown` and `rehype-sanitize` in `frontend/package.json`
- [x] T002 [P] Install `@tailwindcss/typography` and update `frontend/tailwind.config.js`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core retrieval and API endpoints

- [x] T003 Implement `read_documentation(skill_id)` in `backend/src/services/registry.py`
- [x] T004 Implement `GET /api/skills/{id}/documentation` endpoint in `backend/src/api/registration_router.py`
- [x] T005 [P] Update `registration_api.ts` with `getSkillDocumentation(id)` in `frontend/src/services/registration_api.ts`

**Checkpoint**: Foundation ready - documentation can be retrieved from the backend.

---

## Phase 3: User Story 1 - View Rendered Skill Documentation (Priority: P1) 🎯 MVP

**Goal**: Render markdown documentation on the skill card.

**Independent Test**: Manually call the documentation API for a known skill and verify the frontend renders headers and code blocks correctly.

### Tests for User Story 1

- [x] T006 [P] [US1] Unit test for `read_documentation` service in `backend/tests/test_registry_docs.py`
- [x] T007 [P] [US1] Contract test for documentation endpoint in `backend/tests/contract/test_docs_api.py`

### Implementation for User Story 1

- [x] T008 [US1] Add `documentation` state and fetch logic to `SkillCard.tsx`
- [x] T009 [US1] Implement `react-markdown` component with `rehype-sanitize` in `SkillCard.tsx`
- [x] T010 [US1] Apply `prose` class from `@tailwindcss/typography` for documentation styling in `SkillCard.tsx`

**Checkpoint**: User Story 1 complete - Documentation is displayed and rendered correctly.

---

## Phase 4: User Story 2 - Toggle Documentation Visibility (Priority: P2)

**Goal**: Allow expanding/collapsing the documentation view.

**Independent Test**: Verify that the documentation section is hidden by default and expands/collapses when clicking the toggle button.

### Implementation for User Story 2

- [x] T011 [US2] Add `isDocsExpanded` toggle state to `SkillCard.tsx`
- [x] T012 [US2] Implement "View Docs" / "Hide Docs" button in `SkillCard.tsx` actions
- [x] T013 [US2] Add documentation container with 400px max-height, internal scrolling, and 300ms transition in `SkillCard.tsx`

**Checkpoint**: User Story 2 complete - Documentation interface is toggleable and polished.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: UX refinement and error handling

- [x] T014 Implement "No documentation available" fallback message in `SkillCard.tsx`
- [x] T015 Run full validation of `specs/006-skill-markdown-preview/quickstart.md` and verify SC-004 (responsive transitions)