# Implementation Plan: GitHub Direct Skill Folder Input

**Branch**: `005-github-folder-input` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-github-folder-input/spec.md`

## Summary

The goal is to enable direct skill registration via GitHub deep links. Instead of searching a whole repository, users can provide a link directly to a skill folder (e.g., `https://github.com/owner/repo/tree/branch/path`). The system will parse this URL to extract the repo URL, branch, and sub-path, then proceed directly to the security scan and registration workflow for that specific skill.

## Technical Context

**Language/Version**: Python 3.12 (Managed by `uv`)
**Primary Dependencies**: FastAPI (Backend), React + Tailwind CSS (Frontend), `gitpython`
**Storage**: JSON/YAML (Local Registry)
**Testing**: Docker-based testing (Pytest)
**Target Platform**: Docker (Linux-based)
**Project Type**: Web Application (Frontend + Backend)
**Performance Goals**: URL parsing < 100ms
**Constraints**: Security scan mandatory for all registrations
**Scale/Scope**: Transient URL parsing and enhanced registration flow
**NEEDS CLARIFICATION**:
- Handling of `blob` links (direct file links) vs `tree` links (folder links).
- Interaction flow for duplicate detection (blocking vs optional).

## Constitution Check

- [x] Backend is Python 3.12 and uses `uv`?
- [x] Frontend uses React and Tailwind CSS?
- [x] Testing/Execution is Docker-based?
- [x] Secure registration flow implemented? (Maintains Principle IV)

## Project Structure

### Documentation (this feature)

```text
specs/005-github-folder-input/
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
│   │   ├── github.py        # Update parse_github_url and list_repository_skills
│   │   └── registration.py  # Update to support direct sub-path scans
│   └── api/
│       └── registration_router.py
└── tests/               
```

**Structure Decision**: Enhance existing GitHub and Registration services to handle deep-link parsing and direct sub-path processing.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |