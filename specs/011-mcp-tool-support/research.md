# Research: MCP and Tool Support

## Unknowns & Research Tasks

### 1. Integration of `mcp` Python SDK with LangChain
- **Decision**: Wrap MCP tool calls into custom LangChain `BaseTool` classes.
- **Rationale**: This allows the existing agent orchestration logic to treat MCP resources as standard tools.
- **Implementation**: The `ToolService` will handle the lifecycle of MCP server connections and expose them as LangChain-compatible tools.

### 2. Dynamic Loading of Python Functions
- **Decision**: Use `importlib.util` for dynamic module loading.
- **Rationale**: Standard and robust way to load Python files from arbitrary paths at runtime.
- **Validation**: Ensure scripts have a standardized entry point (e.g., `async def run(args: dict) -> dict`).

### 3. Parallel Tool Execution
- **Decision**: Use `asyncio.gather` for tools marked with `parallel_capable: true`.
- **Rationale**: Efficient way to run I/O bound tasks (like multiple web searches) concurrently within the async FastAPI environment.
- **Constraint**: The agent loop needs to be updated to identify groups of independent tool calls.

### 4. API-driven Registry Updates
- **Decision**: Use `aiofiles` for asynchronous file writes to `tools.json` and `mcp.json`.
- **Rationale**: Prevents blocking the event loop during file I/O and ensures persistence.
- **Reliability**: Implement atomic writes (write to temp file then rename) to avoid corruption during crashes.

## Consolidated Findings

- **Architecture**: A singleton `ToolService` will manage the in-memory registry, initialized from JSON files. API calls will update both the memory and the files.
- **Standardization**: Use JSON Schema for tool input/output definition to ensure the LLM receives well-formatted data.
- **Observability**: A custom `ToolLogger` will intercept tool calls and persist them to a log file or database for traceability.
