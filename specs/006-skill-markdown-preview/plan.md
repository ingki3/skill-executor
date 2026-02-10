# Implementation Plan: Skill Markdown Preview

**Branch**: `006-skill-markdown-preview` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-skill-markdown-preview/spec.md`

## Summary

This feature implements a markdown preview for skill documentation directly within the admin dashboard. The backend will be extended with an endpoint to read the `skill.md` (or `SKILL.md`) file from a skill's storage directory. The frontend will integrate `react-markdown` to render this content within a toggleable section on each `SkillCard`, ensuring administrators can quickly reference skill usage and requirements.

## Technical Context

**Language/Version**: Python 3.12 (Managed by `uv`)
**Primary Dependencies**: FastAPI (Backend), React + Tailwind CSS (Frontend), `react-markdown` (Frontend Rendering)
**Storage**: Local Filesystem (cloned skill directories)
**Testing**: Docker-based testing (Pytest, Vitest)
**Target Platform**: Docker (Linux-based)
**Project Type**: Web Application (Frontend + Backend)
**Performance Goals**: Documentation load time < 500ms
**Constraints**: Read-only access to skill directories; XSS prevention during rendering
**Scale/Scope**: Displaying documentation for 10-50 registered skills
**NEEDS CLARIFICATION**:
- Specific library for markdown rendering in React (e.g., `react-markdown` vs `markdown-it`).
- Sanitization strategy for documentation content.
- Handling of images and relative links within the markdown files.

## Constitution Check

- [x] Backend is Python 3.12 and uses `uv`?
- [x] Frontend uses React and Tailwind CSS?
- [x] Testing/Execution is Docker-based?
- [x] Secure registration flow implemented? (Not directly impacted, but documentation files are part of the scanned skill)

## Project Structure

### Documentation (this feature)

```text
specs/006-skill-markdown-preview/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── registration_router.py # Add GET /skills/{id}/docs
│   └── services/
│       └── registry.py            # Add read_documentation method
└── tests/               

frontend/
├── src/
│   ├── components/
│   │   └── SkillCard.tsx          # Add documentation section
│   └── services/
│       └── api.ts                 # Add getSkillDocs call
└── tests/
```

**Structure Decision**: Keep documentation retrieval within the `RegistryService` as it manages the local skill storage paths.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |