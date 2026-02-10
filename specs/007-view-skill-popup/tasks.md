# Tasks: View Skill Popup and Style Fixes

**Input**: Design documents from `/specs/007-view-skill-popup/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Path Conventions

- **Frontend**: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verification of component availability

- [x] T001 [P] Verify imports for `Dialog`, `DialogTitle`, `DialogContent`, and `DialogActions` from `@mui/material` in `frontend/src/components/SkillCard.tsx`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core UI shell for documentation

- [x] T002 Implement `isDialogOpen` state and `handleOpen`/`handleClose` handlers in `frontend/src/components/SkillCard.tsx`

---

## Phase 3: User Story 1 - View Skill Documentation in Popup (Priority: P1) 🎯 MVP

**Goal**: Render documentation in a centered modal with correct styling.

**Independent Test**: Click "View Skill" button and verify a readable modal appears with documentation content.

### Implementation for User Story 1

- [x] T003 [US1] Rename "View Docs" button to "View Skill" and update `handleToggleDocs` to open the dialog in `frontend/src/components/SkillCard.tsx`
- [x] T004 [US1] Implement `MUI Dialog` with `DialogTitle` (Skill Name) and `DialogContent` in `frontend/src/components/SkillCard.tsx`
- [x] T005 [US1] Move `ReactMarkdown` rendering logic into `DialogContent` with `scroll="paper"` in `frontend/src/components/SkillCard.tsx`
- [x] T006 [P] [US1] Apply `prose-slate` and `dark:prose-invert` to the documentation article for contrast fix in `frontend/src/components/SkillCard.tsx`
- [x] T007 [US1] Implement a `CircularProgress` loading indicator within `DialogContent` while fetching documentation in `frontend/src/components/SkillCard.tsx`

**Checkpoint**: User Story 1 complete - Documentation opens in a styled modal with loading state support.

---

## Phase 4: User Story 2 - Documentation Popup Navigation (Priority: P2)

**Goal**: Enable closing the documentation popup via multiple methods.

**Independent Test**: Verify modal closes on backdrop click, ESC key, and close button.

### Implementation for User Story 2

- [x] T008 [US2] Add a "Close" button within `DialogActions` in `frontend/src/components/SkillCard.tsx`
- [x] T009 [US2] Link `onClose` property of the `Dialog` to `handleClose` to support backdrop/ESC closing in `frontend/src/components/SkillCard.tsx`

**Checkpoint**: User Story 2 complete - Modal navigation is fully functional.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Cleanup and UX refinement

- [x] T010 Remove the `Collapse` component and any unused legacy states/logic in `frontend/src/components/SkillCard.tsx`
- [x] T011 [P] Verify responsive behavior (maxWidth="md", fullWidth) on mobile/desktop in `frontend/src/components/SkillCard.tsx`
- [x] T012 Run final validation of `specs/007-view-skill-popup/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 & 2**: Prerequisites for all user stories.
- **Phase 3 (US1)**: Must be implemented before US2 navigation can be tested effectively.
- **Phase 4 (US2)**: Adds navigation to US1 modal.
- **Phase 5**: Final cleanup.

### Parallel Opportunities

- T001 can be checked independently.
- T006 (Styling) can be refined in parallel with T004/T005 implementation.
- T011 (Responsive check) can be done in parallel with T010 cleanup.
