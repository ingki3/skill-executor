# Tasks: MCP and Tool Support

**Feature**: MCP and Tool Support  
**Branch**: `011-mcp-tool-support`  
**Priority**: P1 (Real-time info retrieval is core)  
**Status**: Ready for implementation

## Implementation Strategy

We will follow an incremental delivery approach, starting with the foundational `ToolService` and the P1 user story (Web Search). Each phase results in a testable increment. Security and validation are prioritized in the foundational layer.

## Phase 1: Setup
Initialization of directories and configurations.

- [x] T001 [P] Create tools directory in `backend/src/tools/`
- [x] T002 [P] Initialize empty tool registries in `backend/src/tools/tools.json` and `backend/src/tools/mcp.json`
- [x] T003 Add `mcp` and `aiofiles` dependencies to `backend/pyproject.toml`

## Phase 2: Foundational
Core service logic for loading and validating tools.

- [x] T004 [P] Define tool and execution log models in `backend/src/models/tool.py`
- [x] T005 Create `ToolService` skeleton in `backend/src/services/tool_service.py`
- [x] T006 Implement dynamic registry loading with validation in `backend/src/services/tool_service.py`
- [x] T006a Implement and test critical error/halt behavior for malformed registries in `backend/src/services/tool_service.py`
- [x] T007 Implement LangChain tool wrapper generation in `backend/src/services/tool_service.py`
- [x] T007a [P] Implement semantic indexing of tool descriptions using FAISS in `backend/src/services/tool_service.py`
- [x] T007b [P] Implement asynchronous timeout enforcement in `backend/src/services/tool_service.py`

## Phase 3: [US1] Real-time Information Retrieval (Priority: P1)
Enabling the agent to fetch current information via web search.

**Independent Test**: Agent answers "What is the current price of Bitcoin?" by calling the web search tool.

- [x] T008 [P] [US1] Implement web search utility in `backend/src/tools/web_search.py`
- [x] T009 [US1] Register `web_search` tool in `backend/src/tools/tools.json`
- [x] T010 [US1] Integrate `ToolService` into agent orchestration in `backend/src/services/agent_service.py`
- [x] T010a [US1] Implement 'request_human_input' tool logic in `backend/src/tools/request_human_input.py`

## Phase 4: [US2] Automated Task Execution via Code (Priority: P2)
Allowing the agent to execute scripts for computation.

**Independent Test**: Agent calculates a complex mathematical sequence by writing and running a Python script.

- [x] T011 [P] [US2] Implement code execution utility in `backend/src/tools/code_execution.py`
- [x] T012 [US2] Register `code_execution` tool in `backend/src/tools/tools.json`
- [x] T013 [US2] Implement parallel execution logic using `asyncio.gather` in `backend/src/services/tool_service.py`

## Phase 5: [US3] Dynamic Tool Extension (Priority: P3)
API management of the tool registry and observability.

**Independent Test**: Register a new tool via API and observe it being used by the agent in the next request.

- [x] T014 [P] [US3] Implement tool management API routes in `backend/src/api/tools.py`
- [x] T015 [US3] Implement atomic registry persistence using `aiofiles` in `backend/src/services/tool_service.py`
- [x] T016 [US3] Implement detailed tool execution logging in `backend/src/services/tool_service.py`

## Phase 6: [US4] External Resource Access via MCP (Priority: P3)
Integrating with remote MCP servers.

**Independent Test**: Connect to a remote MCP server and retrieve data from its resources.

- [x] T017 [US4] Implement MCP client lifecycle management in `backend/src/services/tool_service.py`
- [x] T018 [US4] Implement `MCPTool` wrapper for LangChain in `backend/src/services/tool_service.py`

## Phase 7: Polish & Cross-cutting Concerns
Final verification and performance tuning.

- [x] T019 Verify total execution overhead is under 200ms (SC-003)
- [x] T020 Ensure 100% of tool executions are traceable in logs (SC-006)
- [x] T021 Verify tool selection accuracy (90% target) using a test dataset (SC-001)
- [x] T022 Verify new tool registration time is under 5 minutes (SC-002)
- [x] T023 Verify agent falls back to human input when information is missing (SC-005)

## Dependencies

- Phase 2 (Foundational) MUST be completed before any User Story phases.
- Phase 3 (US1) is the MVP and SHOULD be completed before US2-US4.
- US3 and US4 are independent of each other and can be executed in parallel.

## Parallel Execution Examples

- **Setup & Foundational**: T001, T002, T004 can start together.
- **US Implementation**: T008 (US1) and T011 (US2) can be implemented in parallel if ToolService skeleton (T005) is ready.
- **API**: T014 can be developed in parallel with US1/US2 backend logic.
