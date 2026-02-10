# Implementation Plan: Unified Docker Image and Skill Testing

**Branch**: `002-unified-docker-image` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-unified-docker-image/spec.md`

## Summary

The goal is to unify the frontend and backend into a single Docker image while maintaining separate service accessibility via multiple ports. The implementation will involve a multi-stage Docker build, a UI-based selection mechanism for registering skills from the `awesome-claude-skills` repository, and the use of Docker volumes for persistent data storage.

## Technical Context

**Language/Version**: Python 3.12 (Managed by `uv`)
**Primary Dependencies**: FastAPI (Backend), React + Tailwind CSS (Frontend)
**Storage**: FAISS (Vector Store), JSON/YAML (Local Registry), Docker Volumes
**Testing**: Docker-based testing
**Target Platform**: Docker (Linux-based)
**Project Type**: Web Application (Frontend + Backend)
**Performance Goals**: System initialization < 15s
**Constraints**: Single Docker image; Multiple exposed ports; Security scan for registration
**Scale/Scope**: Local skill registry, extensible architecture

## Constitution Check

- [x] Backend is Python 3.12 and uses `uv`?
- [x] Frontend uses React and Tailwind CSS?
- [x] Testing/Execution is Docker-based?
- [x] Secure registration flow implemented?

## Project Structure

### Documentation (this feature)

```text
specs/002-unified-docker-image/
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
│   ├── services/
│   ├── api/
│   └── core/            
└── tests/               

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

Dockerfile               # New Unified Dockerfile (multi-stage)
docker-compose.yml       # Updated for unified image and volumes
```

**Structure Decision**: Multi-stage Dockerfile that builds React assets and copies them into a Python 3.12 runtime environment. The runtime will execute both the FastAPI server and (optionally) a lightweight static server if not handled by FastAPI directly, exposing both ports.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |