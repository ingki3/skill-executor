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
- 008-view-skill-style-fix: Added Python 3.12 (Managed by `uv`) + React + Tailwind CSS (Frontend), MUI (UI Components)
- 008-view-skill-style-fix: Added Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend)
- 007-view-skill-popup: Added Python 3.12 (Managed by `uv`) + FastAPI (Backend), React + Tailwind CSS (Frontend), MUI (Dialog)


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
