# Implementation Plan: Human-in-the-Loop (HITL) Execution Mode

**Branch**: `009-hitl-execution-mode` | **Date**: 2026-02-08 | **Spec**: [/specs/009-hitl-execution-mode/spec.md](spec.md)
**Input**: Feature specification from `/specs/009-hitl-execution-mode/spec.md`

## Summary

Implement an interactive execution mode where the agent can pause to request human input (HITL) or run autonomously. This involves managing persistent execution sessions, conversation history, and real-time communication between the backend agent loop and the frontend UI.

## Technical Context

**Language/Version**: Python 3.12 (Managed by `uv`)
**Primary Dependencies**: FastAPI (Backend), React + Tailwind CSS (Frontend), LangChain (Agent Memory)
**Storage**: FAISS (Vector Store), JSON/YAML (Local Registry), In-memory Session Registry
**Testing**: Docker-based testing (Pytest for backend)
**Target Platform**: Docker (Linux-based)
**Project Type**: Web Application (Frontend + Backend)
**Performance Goals**: Session persistence across UI navigation, <1s response time for status updates
**Constraints**: 30-minute session timeout, Max 5 concurrent sessions
**Scale/Scope**: Interactive execution dashboard

### Needs Clarification (Research Tasks)
1. **Interruptible Agent Loop**: How to cleanly pause a LangChain-based ReACT loop to wait for user input without blocking server resources? [NEEDS CLARIFICATION]
2. **Real-time Communication**: Should we use WebSockets or SSE for streaming **Execution Reasoning** and input requests to the frontend? [NEEDS CLARIFICATION]
3. **Session Recovery**: Best practice for restoring agent state from memory if the backend service restarts? [NEEDS CLARIFICATION]

## Constitution Check

- [x] Backend is Python 3.12 and uses `uv`?
- [x] Frontend uses React and Tailwind CSS?
- [x] Testing/Execution is Docker-based?
- [x] Secure registration flow implemented?

## Project Structure

### Documentation (this feature)

```text
specs/009-hitl-execution-mode/
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
│   ├── models/          # Session & Message models
│   ├── services/        # Execution & Session management
│   ├── api/             # Execution endpoints (REST + WS)
│   └── core/            # Agent loop logic
└── tests/               # Docker-based tests

frontend/
├── src/
│   ├── components/      # ExecutionMonitor, InputPrompt
│   ├── pages/           # ExecutionDashboard
│   └── services/        # ExecutionAPI client
└── tests/
```

**Structure Decision**: Web application structure with independent backend/frontend services and shared Docker orchestration.

