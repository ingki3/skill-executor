# skill-executor Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-06

## Active Technologies
- Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend), FAISS (Vector DB), `gitpython` (GitHub integration), `langchain` (ReACT orchestration) (001-skill-executor-agent)
- FAISS (Vector Store), JSON/YAML (Local Registry in `.skills/`) (001-skill-executor-agent)
- FAISS (Vector Store), JSON/YAML (Local Registry) (002-unified-docker-image)
- FAISS (Vector Store), JSON/YAML (Local Registry), Docker Volumes (002-unified-docker-image)
- FAISS (Vector Store), JSON/YAML (Local Registry), Temporary storage for pending registrations (003-skill-risk-review)
- FAISS (Vector Store), JSON/YAML (Local Registry), JSON-based persistence for `.pending_registrations/` (003-skill-risk-review)
- Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend), `gitpython` (005-github-folder-input)
- Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend), `react-markdown` (Frontend Rendering) (006-skill-markdown-preview)
- Local Filesystem (cloned skill directories) (006-skill-markdown-preview)
- Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend), MUI (Dialog) (007-view-skill-popup)
- N/A (UI-only change, uses existing `/skills/{id}/documentation` endpoint) (007-view-skill-popup)
- Python 3.12 (Managed by `uv`) + React + Tailwind CSS (Frontend), MUI (UI Components) (008-view-skill-style-fix)
- N/A (UI-only change) (008-view-skill-style-fix)
- Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend), LangChain (Agent Memory), FAISS (Vector Store) (009-hitl-execution-mode)
- FAISS (Vector Store), JSON/YAML (Local Registry), In-memory Session Store (with Redis-ready architecture) (009-hitl-execution-mode)
- FAISS (Vector Store), JSON/YAML (Local Registry), In-memory Session Registry (009-hitl-execution-mode)
- Python 3.12 (Managed by `uv`) + FastAPI (Backend), PyYAML (YAML parsing), Pydantic (Validation) (010-separate-prompt-yaml)
- Local Filesystem (`backend/src/prompt/*.yaml`) (010-separate-prompt-yaml)

- Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend), FAISS (Vector DB), `gitpython` (GitHub integration) (001-skill-executor-agent)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.12 (Managed by `uv`): Follow standard conventions

## Recent Changes
- 010-separate-prompt-yaml: Added Python 3.12 (Managed by `uv`) + FastAPI (Backend), PyYAML (YAML parsing), Pydantic (Validation)
- 009-hitl-execution-mode: Added Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend), LangChain (Agent Memory)
- 009-hitl-execution-mode: Added Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend), LangChain (Agent Memory), FAISS (Vector Store)


<!-- MANUAL ADDITIONS START -->
## Git Repository Policy
- **Sync**: `main` branch should be periodically synchronized into `dev`.
- **Feature Branches**: All feature branches must be merged into `dev` only.
- **Main Merge**: Merges into `main` must only come from the `dev` branch.
<!-- MANUAL ADDITIONS END -->
