# Implementation Plan: Local Skill Registration

**Branch**: `004-local-skill-registration` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-local-skill-registration/spec.md`

## Summary

The goal is to enable registration of skills from the local server filesystem. This involves extending the "Search Repo" functionality to accept absolute local paths, listing subdirectories as potential skills, and processing selected folders through the existing security-verified registration workflow (metadata extraction, risk analysis, and registry addition). To ensure security, local path searching will be restricted to the project root directory.

## Technical Context

**Language/Version**: Python 3.12 (Managed by `uv`)
**Primary Dependencies**: FastAPI (Backend), React + Tailwind CSS (Frontend)
**Storage**: FAISS (Vector Store), JSON/YAML (Local Registry)
**Testing**: Docker-based testing (Pytest, Vitest)
**Target Platform**: Docker (Linux-based)
**Project Type**: Web Application (Frontend + Backend)
**Performance Goals**: Local directory listing < 500ms
**Constraints**: Security scan mandatory for all registrations; Path boundary restricted to project root (Clarification Q1); Duplicate resolution via overwrite confirmation (Clarification Q2)
**Scale/Scope**: Server-side directory traversal within project root; Integration with `RegistrationService`

## Constitution Check

- [x] Backend is Python 3.12 and uses `uv`?
- [x] Frontend uses React and Tailwind CSS?
- [x] Testing/Execution is Docker-based?
- [x] Secure registration flow implemented? (Local skills also undergo security scans)

## Project Structure

### Documentation (this feature)

```text
specs/004-local-skill-registration/
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
│   ├── services/
│   │   ├── local_fs.py      # New service for FS operations
│   │   └── registration.py  # Update to handle local paths
│   └── api/
│       └── registration_router.py # Add local search endpoints
└── tests/               

frontend/
├── src/
│   ├── services/
│   │   └── registration_api.ts # Add local search calls
│   └── pages/
│       └── Dashboard.tsx       # UI update for path input
```

**Structure Decision**: Add a dedicated `LocalFSService` to handle directory listing and validation safely, keeping it separate from the GitHub-specific logic.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |