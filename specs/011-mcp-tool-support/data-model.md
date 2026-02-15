# Data Model: MCP and Tool Support

## Entities

### ToolDefinition
Represents a tool available to the agent.
- **name**: string (unique identifier)
- **description**: string (LLM instructions)
- **type**: enum ("local", "mcp")
- **input_schema**: object (JSON Schema)
- **output_schema**: object (JSON Schema)
- **parallel_capable**: boolean (default: false)
- **config**: object (Type-specific configuration)

### LocalToolConfig
- **script_path**: string (relative to `backend/src/tools/`)
- **entrypoint**: string (function name, default: "run")

### MCPToolConfig
- **server_name**: string
- **command**: string (e.g., "npx", "python")
- **args**: list of strings
- **env**: object (optional environment variables)

### ToolExecutionLog
- **id**: UUID
- **timestamp**: ISO8601 string
- **tool_name**: string
- **input**: object
- **output**: object (or error message)
- **duration_ms**: integer
- **status**: enum ("success", "error")

### ToolResponse
The standardized envelope for all tool execution results.
- **status**: enum ("success", "error")
- **data**: object (The actual tool result output)
- **message**: string (Optional success summary or error details)
- **execution_id**: UUID (Reference to the corresponding ToolExecutionLog)

## State Transitions

1. **Registration**: Validates schema and script existence -> Persists to `tools.json`/`mcp.json` -> Reloads `ToolService`.
2. **Execution**: Agent selects tool -> Input validated against schema -> Execution triggered (Local/MCP) -> Result logged -> Result returned to Agent.
