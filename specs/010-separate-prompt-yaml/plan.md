# Implementation Plan: Separate Prompt YAML Management

**Branch**: `010-separate-prompt-yaml` | **Date**: 2026-02-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/010-separate-prompt-yaml/spec.md`

## Summary

Centralize all LLM prompts into a dedicated `backend/src/prompt/` directory using YAML files. Implement a robust `PromptLoader` utility to read, cache, and format these templates, replacing all hardcoded prompt strings in the backend services.

## Technical Context

**Language/Version**: Python 3.12 (Managed by `uv`)
**Primary Dependencies**: FastAPI (Backend), PyYAML (YAML parsing), Pydantic (Validation)
**Storage**: Local Filesystem (`backend/src/prompt/*.yaml`)
**Testing**: Pytest (Unit tests for template loading and formatting)
**Target Platform**: Docker (Linux-based)
**Project Type**: Backend Refactoring
**Performance Goals**: Sub-millisecond prompt retrieval from cache
**Constraints**: Zero hardcoded prompts allowed in `.py` files post-migration
**Scale/Scope**: All backend services (registration, execution, security)

## Constitution Check

- [x] Backend is Python 3.12 and uses `uv`?
- [x] Frontend uses React and Tailwind CSS?
- [x] Testing/Execution is Docker-based?
- [x] Secure registration flow implemented?

## Project Structure

### Documentation (this feature)

```text
specs/010-separate-prompt-yaml/
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
│   ├── prompt/          # Centralized YAML prompts
│   ├── services/        # Migration of hardcoded strings
│   ├── core/            # PromptLoader implementation
│   └── ...
└── tests/               # Loader unit tests
```

**Structure Decision**: Place `PromptLoader` in `core/` as it's a cross-cutting utility. Place templates in `src/prompt/` for easy packaging.

