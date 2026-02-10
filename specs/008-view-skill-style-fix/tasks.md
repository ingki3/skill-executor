# Tasks: View Skill Style and Layout Fix

**Input**: Design documents from `/specs/008-view-skill-style-fix/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Path Conventions

- **Frontend**: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verification of component state

- [x] T001 [P] Verify `frontend/src/components/SkillCard.tsx` has correct theme-aware typography imports from `@mui/material`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure baseline popup logic is stable

- [x] T002 Verify existing `isDialogOpen` state and `handleOpenDialog` handler in `frontend/src/components/SkillCard.tsx`

---

## Phase 3: User Story 1 - Improved Text Legibility (Priority: P1) 🎯 MVP

**Goal**: Ensure documentation text follows system theme for high contrast.

**Independent Test**: Switch between Light and Dark modes while the "View Skill" popup is open; verify text remains readable and matches theme expectations.

### Implementation for User Story 1

- [x] T003 [US1] Apply theme-aware classes to the documentation container in `frontend/src/components/SkillCard.tsx` (ensure `prose-slate` and `dark:prose-invert` are present)
- [x] T004 [US1] Ensure `DialogContent` background and text properties satisfy high contrast readability in both themes in `frontend/src/components/SkillCard.tsx`

**Checkpoint**: User Story 1 complete - Documentation text is legible in both themes.

---

## Phase 4: User Story 2 - Clear Separation of Name and Description (Priority: P2)

**Goal**: Add skill description to the popup with proper spacing and hierarchy.

**Independent Test**: Open the popup and verify the skill description appears below the title with a clear gap and secondary styling.

### Implementation for User Story 2

- [x] T005 [US2] Insert `skill.description` at the top of `DialogContent` in `frontend/src/components/SkillCard.tsx`
- [x] T006 [US2] Apply secondary styling to the description (e.g., `variant="body2"`, `color="text.secondary"`, `mb: 2`) in `frontend/src/components/SkillCard.tsx`
- [x] T007 [US2] Ensure a vertical line break/gap between the `DialogTitle` and the description in `frontend/src/components/SkillCard.tsx`

**Checkpoint**: User Story 2 complete - Layout hierarchy is improved with name, description, and docs separated.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and cleanup

- [x] T008 [P] Perform visual audit of spacing (min 16px gap) per `SC-002` in `frontend/src/components/SkillCard.tsx`
- [x] T009 Run final validation of `specs/008-view-skill-style-fix/quickstart.md` and verify WCAG contrast ratios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 & 2**: Baseline verification.
- **Phase 3 (US1)**: Focuses on text color/contrast.
- **Phase 4 (US2)**: Focuses on content layout and hierarchy.
- **Phase 5**: Final Polish.

### Parallel Opportunities

- T001 and T002 can be checked simultaneously.
- T008 can be performed after T007 is done.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Verify setup and foundational logic.
2. Complete US1 (Legibility fixes).
3. **STOP and VALIDATE**: Verify contrast in both themes.

### Incremental Delivery

1. Foundation ready.
2. US1 Legibility → Test independently.
3. US2 Layout → Test independently.
4. Final Polish.
