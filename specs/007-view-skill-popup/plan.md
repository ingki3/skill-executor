# Implementation Plan: View Skill Popup and Style Fixes

**Branch**: `007-view-skill-popup` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-view-skill-popup/spec.md`

## Summary

This feature replaces the inline `Collapse` documentation view in the `SkillCard` with a centered `MUI Dialog` (modal). This provides a more focused reading experience. Additionally, the "View Docs" button is renamed to "View Skill", and text contrast issues are resolved by explicitly applying high-contrast typography classes within the modal.

## Technical Context

**Language/Version**: Python 3.12 (Managed by `uv`)
**Primary Dependencies**: FastAPI (Backend), React + Tailwind CSS (Frontend), MUI (Dialog)
**Storage**: N/A (UI-only change, uses existing `/skills/{id}/documentation` endpoint)
**Testing**: Docker-based testing (Cypress/Vitest for frontend UI)
**Target Platform**: Docker (Linux-based)
**Project Type**: Web Application (Frontend)
**Performance Goals**: Popup open time < 100ms (once data is fetched)
**Constraints**: Must maintain Material Design principles and ensure WCAG AA contrast levels
**Scale/Scope**: Frontend component refactor

## Constitution Check

- [x] Backend is Python 3.12 and uses `uv`?
- [x] Frontend uses React and Tailwind CSS?
- [x] Testing/Execution is Docker-based?
- [x] Secure registration flow implemented?

## Project Structure

### Documentation (this feature)

```text
specs/007-view-skill-popup/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── ui-flow.json
└── tasks.md             # (Next step: /speckit.tasks)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   └── SkillCard.tsx          # Modify: rename button, remove Collapse, add Dialog trigger
└── tests/               

backend/
└── (No changes required for this feature)
```

**Structure Decision**: Frontend refactor within `SkillCard.tsx` or moving the documentation popup to a dedicated component.

## Complexity Tracking

*No violations.*