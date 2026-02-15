# Implementation Plan: MCP and Tool Support

**Branch**: `011-mcp-tool-support` | **Date**: 2026-02-15 | **Spec**: [/specs/011-mcp-tool-support/spec.md](/specs/011-mcp-tool-support/spec.md)
**Input**: Feature specification from `/specs/011-mcp-tool-support/spec.md`

## Summary

Improve the Skill Executor Agent to support Model Context Protocol (MCP) and dynamic tool loading. The executor will be able to load tool definitions from `tools.json` and `mcp.json`, and execute either local Python scripts or remote MCP-compliant services. This architecture enables the agent to access real-time information (web search) and perform complex tasks (code execution) without hardcoding logic into the agent core. The system will also provide API endpoints for dynamic tool management and detailed logging for observability.

## Technical Context

**Language/Version**: Python 3.12 (Managed by `uv`)
**Primary Dependencies**: FastAPI (Backend), LangChain (Agent Orchestration), `mcp` Python SDK (MCP Client), `pydantic` (Validation)
**Storage**: JSON for tool registry (`tools.json`, `mcp.json`), Local Filesystem for tool scripts (`backend/src/tools/`), FAISS (Vector Store)
**Testing**: Docker-based testing (Pytest for backend)
**Target Platform**: Docker (Linux-based)
**Project Type**: Backend service extension
**Performance Goals**: Tool selection and initialization < 200ms
**Constraints**: Trusted environment for local scripts; immediate halt on configuration errors
**Scale/Scope**: Local and remote tool integration for the Skill Executor

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Backend is Python 3.12 and uses `uv`?
- [x] Frontend uses React and Tailwind CSS?
- [x] Testing/Execution is Docker-based?
- [x] Secure registration flow implemented? (Not directly applicable to tool registry but principles followed)

## Project Structure

### Documentation (this feature)

```text
specs/011-mcp-tool-support/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (relevant parts)

```text
backend/
├── src/
│   ├── services/
│   │   ├── agent_service.py   # Updated: Tool integration
│   │   └── tool_service.py    # NEW: Tool registry & execution management
│   ├── tools/                 # NEW: Tool scripts and configs
│   │   ├── tools.json         # Local tool registry
│   │   ├── mcp.json           # MCP server registry
│   │   ├── code_execution.py  # Built-in tool
│   │   └── web_search.py      # Built-in tool
└── tests/
    └── unit/
        └── test_tool_service.py
```

**Structure Decision**: Integrated into existing backend structure, with a new `tools/` directory for configuration and script-based tool implementations. API endpoints will be added to the existing `api/` structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

(No violations)
