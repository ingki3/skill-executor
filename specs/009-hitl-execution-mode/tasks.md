# Tasks: Human-in-the-Loop (HITL) Execution Mode

**Feature**: Human-in-the-Loop (HITL) Execution Mode
**Implementation Plan**: [plan.md](plan.md)
**Status**: Initialized
**Strategy**: MVP First (US1) -> Full Automation (US2) -> Persistence & Polish (US3)

## Phase 1: Setup

- [X] T001 [P] Create session storage directory `.skill-executor-data/sessions/`
- [X] T002 [P] Install `websockets` dependency for FastAPI in `backend/pyproject.toml`
- [X] T003 [P] Setup WebSocket client infrastructure in `frontend/src/services/execution_api.ts`

## Phase 2: Foundational

- [X] T004 [P] Implement `ExecutionSession` and `ExecutionMessage` Pydantic models in `backend/src/models/execution.py`
- [X] T005 [P] Create `SessionRegistry` service for in-memory session tracking in `backend/src/services/session_registry.py`
- [X] T006 Implement base `ExecutionService` with LangChain `AgentExecutor` skeleton in `backend/src/services/execution.py`
- [X] T007 Define WebSocket event types and schemas in `backend/src/api/websocket_schemas.py`

## Phase 3: User Story 1 - Interactive Skill Execution (HITL)

**Goal**: Enable agent to pause for user input and resume via WebSockets.
**Independent Test**: Execute a skill that triggers `RequestInputTool`, verify WebSocket `request_input` event, send `user_response`, and verify agent resumes.

- [X] T008 [US1] Create custom `RequestInputTool` that raises `HumanInterrupt` exception in `backend/src/core/tools.py`
- [X] T009 [US1] Implement `InterruptibleAgentLoop` logic to catch `HumanInterrupt` and save state in `backend/src/core/agent_loop.py`
- [X] T010 [US1] Create WebSocket endpoint `WS /ws/execution/{session_id}` in `backend/src/api/execution_router.py`
- [X] T011 [US1] Implement `POST /api/execution/start` with HITL mode support in `backend/src/api/execution_router.py`
- [X] T012 [P] [US1] Create `ExecutionMonitor` component to display reasoning steps in `frontend/src/components/ExecutionMonitor.tsx`
- [X] T013 [P] [US1] Create `InputPrompt` component for user feedback in `frontend/src/components/InputPrompt.tsx`
- [X] T014 [US1] Integrate WebSocket stream into `ExecutionDashboard` page in `frontend/src/pages/ExecutionDashboard.tsx`

## Phase 4: User Story 2 - Autonomous Skill Execution

**Goal**: Support hands-off execution with fallback strategies.
**Independent Test**: Run a skill with HITL disabled, verify it completes without pausing, and terminates within 10 steps.

- [X] T015 [US2] Implement max step enforcement (10 steps) in `backend/src/core/agent_loop.py`
- [X] T016 [US2] Add autonomous mode routing logic to `ExecutionService` in `backend/src/services/execution.py`
- [X] T017 [US2] Implement fallback strategy (fail with descriptive error) when ambiguity is met in autonomous mode in `backend/src/core/agent_loop.py`
- [X] T018 [P] [US2] Add HITL/Autonomous toggle to skill execution dialog in `frontend/src/components/ExecutionDialog.tsx`

## Phase 5: User Story 3 - Session Context Persistence

**Goal**: Persist session history and handle timeouts.
**Independent Test**: Start session, refresh browser, verify history is restored from `GET /api/execution/sessions/{session_id}`.

- [X] T019 [US3] Implement JSON serialization for `SessionRegistry` in `backend/src/services/session_registry.py`
- [X] T020 [US3] Add `GET /api/execution/sessions/{session_id}` endpoint in `backend/src/api/execution_router.py`
- [X] T021 [US3] Implement background task for 30-minute session cleanup in `backend/src/services/session_registry.py`
- [X] T022 [US3] Implement session restoration logic in `frontend/src/pages/ExecutionDashboard.tsx`

## Phase 6: Polish & Cross-Cutting

- [X] T023 Implement **Execution Reasoning** streaming with token-by-token display in `frontend/src/components/ExecutionMonitor.tsx`
- [X] T024 Add error handling for WebSocket disconnections in `frontend/src/services/execution_api.ts`
- [X] T025 Ensure 5-session concurrency limit is enforced and returns a 429 error in `backend/src/services/session_registry.py`

## Dependencies

1. US1 depends on Phase 1 & 2.
2. US2 depends on US1 (for base loop).
3. US3 depends on US1 & US2.

## Parallel Execution Examples

- **Backend Development**: T004, T005, T007, T008 can be done in parallel.
- **Frontend Development**: T012, T013 can be done in parallel with Backend T009, T010.

## Implementation Strategy

1. **MVP (US1)**: Focus on the WebSocket connection and the `RequestInputTool`. This proves the core interactive loop.
2. **Expansion (US2)**: Add the autonomous constraints once the loop is stable.
3. **Robustness (US3)**: Add persistence and cleanup to make the system production-ready.
