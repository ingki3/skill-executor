# Implementation Plan: Skill Risk Review

**Branch**: `003-skill-risk-review` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-skill-risk-review/spec.md`

## Summary

The Skill Risk Review feature implements an administrative workflow for bulk skill registration. It extends the security scan process to provide detailed risk findings and introduces a persistent "Registration Queue" where administrators must manually approve or reject every skill—regardless of its automated safety status—before it is added to the permanent registry.

## Technical Context

**Language/Version**: Python 3.12 (Managed by `uv`)
**Primary Dependencies**: FastAPI (Backend), React + Tailwind CSS (Frontend)
**Storage**: FAISS (Vector Store), JSON/YAML (Local Registry), JSON-based persistence for `.pending_registrations/`
**Testing**: Docker-based testing (Pytest, Vitest)
**Target Platform**: Docker (Linux-based)
**Project Type**: Web Application (Frontend + Backend)
**Performance Goals**: Security scan completion < 30s per batch; UI responsiveness < 200ms
**Constraints**: Mandatory security scan; Mandatory manual judgment for all skills (Clarification Q2)
**Scale/Scope**: Local admin-only workflow; intermediate state management for pending skills

## Constitution Check

- [x] Backend is Python 3.12 and uses `uv`?
- [x] Frontend uses React and Tailwind CSS?
- [x] Testing/Execution is Docker-based?
- [x] Secure registration flow implemented? (Enhances Principle IV)

## Project Structure

### Documentation (this feature)

```text
specs/003-skill-risk-review/
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
│   ├── models/
│   │   └── registration.py  # New models for Batch and Queue Item
│   ├── services/
│   │   ├── registration.py  # Update to handle pending state
│   │   ├── security.py      # Update to return detailed findings
│   │   └── batch_store.py   # New service for queue persistence
│   └── api/
│       └── registration_router.py # Endpoints for batches and judgment
└── tests/               

frontend/
├── src/
│   ├── components/
│   │   ├── RegistrationQueue.tsx # Listing of pending items
│   │   ├── RiskDetailsPanel.tsx  # Detailed finding display
│   │   └── CodeReviewDialog.tsx  # Code inspection view
│   ├── pages/
│   │   └── Dashboard.tsx         # Integration of queue UI
│   └── services/
│       └── registration_api.ts   # New batch and judgment calls
```

**Structure Decision**: Use a dedicated file-based store (`.pending_registrations/`) for queue persistence to ensure it survives container restarts as clarified.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |