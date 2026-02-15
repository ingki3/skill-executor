# Feature Specification: MCP and Tool Support for Skill Executor

**Feature Branch**: `011-mcp-tool-support`  
**Created**: 2026-02-15  
**Status**: Draft  
**Input**: User description: "Improve skill executor to support MCP or Tools based on tool_mcp_use.md"

## Clarifications
### Session 2026-02-15
- Q: What is the required level of isolation for local Python/Shell script execution in this version? → A: None (Trusted Environment)
- Q: How should the system handle additions or updates to these files during runtime? → A: API-driven Updates (Tools are registered via an API endpoint that persists changes to JSON)
- Q: What is the minimum required observability for tool executions in this feature? → A: Tool Execution Log (Detailed log of every tool call, including input arguments and full output/errors)
- Q: What is the desired behavior when the system encounters a malformed or missing tool registry file during startup or runtime update? → A: Throw Error and Halt (The service fails to start or the update API returns an error; requires manual fix)
- Q: Should the executor support parallel execution of tools when multiple tools are selected for a single task? → A: Configurable per Tool (Allow specific tools to be marked as parallel-capable in tools.json)
- Q: How should the system handle a tool execution that exceeds a defined time limit? → A: Configurable Timeout (Each tool has a `timeout` field in its config; if exceeded, the execution is killed and an error is returned to the agent)
- Q: What mechanism should be used to help the agent resolve ambiguity when multiple tools seem applicable? → A: Natural Language Instructions (Use the `description` field to provide explicit instructions on when to prefer one tool over another)
- Q: What strategy should be used to prevent registry corruption when multiple API requests attempt to update the configuration files simultaneously? → A: Sequential Queue (All update requests are placed in a background queue and processed one by one)
- Q: Which transport protocols should be supported for MCP? → A: stdio, SSE, and HTTP.
- Q: How should the agent "reload" tools after an API update? → A: Hot-reload (Immediate in-memory update after API write).
- Q: What security is required for the Tool Registration API? → A: API Key (Simple header-based token).
- Q: How will the "90% accuracy" success criterion be verified? → A: Automated test suite with 50+ gold-standard query/tool mappings.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Real-time Information Retrieval (Priority: P1)

As a user, I want the Skill Executor to search the web when I ask for information that is not in its training data, so that I receive accurate and up-to-date answers.

**Why this priority**: Core value of an agentic executor is the ability to fetch current information beyond its static knowledge.

**Independent Test**: Can be tested by asking the agent about a very recent news event. The agent should identify the need for a tool, call the search tool, and provide an answer based on the search results.

**Acceptance Scenarios**:

1. **Given** the `web_search` tool is registered in `tools.json`, **When** the user asks about today's weather in Seoul, **Then** the agent calls the `web_search` tool and returns the current weather.
2. **Given** the `web_search` tool is registered, **When** the user asks a general knowledge question (e.g., "What is the capital of France?"), **Then** the agent answers directly without unnecessarily calling the search tool.

---

### User Story 2 - Automated Task Execution via Code (Priority: P2)

As a user, I want the agent to execute Python code or shell scripts when a skill requires computation or system interaction, so that complex tasks can be automated.

**Why this priority**: Enables the agent to perform actions and process data rather than just answering questions.

**Independent Test**: Provide a skill that requires calculating a complex mathematical sequence. The agent should write and execute a Python script to find the result.

**Acceptance Scenarios**:

1. **Given** the `code_execution` tool is registered, **When** the user provides a task requiring data processing (e.g., "Summarize this CSV file"), **Then** the agent executes a script to process the data and returns the summary.
2. **Given** the `code_execution` tool is registered, **When** a script execution fails, **Then** the agent reports the error clearly to the user.

---

### User Story 3 - Dynamic Tool Extension (Priority: P3)

As a developer, I want to add new tools to the executor by simply adding a configuration entry and a Python script, so that I can extend the system's capabilities without modifying the core agent logic.

**Why this priority**: Ensures the system is maintainable and extensible for future needs.

**Independent Test**: Add a dummy "hello_world" tool to `tools.json` and a corresponding `.py` file. Verify the agent can recognize and use it when prompted.

**Acceptance Scenarios**:

1. **Given** a new tool definition is added to `tools.json` via API, **When** the agent starts or reloads, **Then** it successfully loads the new tool into its available tools list.
2. **Given** a tool is removed from `tools.json` via API, **When** the agent starts or reloads, **Then** it no longer attempts to use that tool.

---

### User Story 4 - External Resource Access via MCP (Priority: P3)

As a system administrator, I want to connect the Skill Executor to external MCP servers, so that the agent can access specialized resources and tools hosted elsewhere.

**Why this priority**: Enables ecosystem integration and reuse of existing MCP-compliant services.

**Independent Test**: Configure a mock MCP server in `mcp.json`. Verify the agent can list and use resources from that server.

**Acceptance Scenarios**:

1. **Given** an MCP server URL is configured in `mcp.json`, **When** the agent initializes, **Then** it establishes a connection to the MCP server.
2. **Given** an active MCP connection, **When** a user request requires a resource from the MCP server, **Then** the agent successfully retrieves and uses that resource.

### Edge Cases

- **Tool Timeout**: The system MUST support a configurable timeout for each tool. If the execution exceeds this limit, the process is terminated and a standardized timeout error is returned to the agent.
- **Ambiguous Tool Choice**: Ambiguity is resolved via Natural Language Instructions within the tool's `description` field. Authors should provide explicit guidance (e.g., "Use this tool for X, but prefer tool Y if Z is present") to guide the agent's selection.
- **Security**: Local tools located in `backend/src/tools/` are treated as trusted; no additional process-level isolation or sandboxing is required for this version. Filesystem access is implicitly restricted to the application's runtime permissions.
- **Missing Configuration**: The system MUST throw a critical error and halt initialization if `tools.json` or `mcp.json` is missing or malformed (invalid JSON or schema violation).
- **Missing Tool Script**: If a tool is registered but its script is missing from `backend/src/tools/`, the system MUST return a standardized `ToolExecutionError` to the agent.
- **Runtime Update Conflict**: All API-driven updates to the tool registry MUST be processed through a sequential background queue to prevent file corruption and ensure state consistency.
- **Tool Failure Traceability**: Ensure that when a tool fails, the specific input that caused the failure is logged for debugging.
- **Concurrency Conflicts**: If parallel execution is enabled for a tool, the system MUST ensure thread/process safety for that tool's execution.
- **MCP Connection Drop**: If a connection to an external MCP server is lost, the system MUST attempt up to 3 reconnections before returning a `ServiceUnavailable` error to the agent.
- **Log Rotation**: Tool execution logs MUST follow a daily rotation policy, retaining logs for a minimum of 30 days.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load tool definitions dynamically from `backend/src/tools/tools.json` at startup.
- **FR-002**: System MUST support dynamic loading and execution of Python-based tools located in `backend/src/tools/`.
- **FR-003**: System MUST provide a mechanism to connect to external MCP servers based on configurations in `mcp.json`, utilizing the official `mcp` Python SDK (v1.0.0+).
- **FR-004**: The Agent MUST be able to select the appropriate tool based on the `description` field provided in the tool configuration, leveraging semantic similarity where applicable.
- **FR-005**: System MUST validate tool inputs and outputs against the JSON Schema defined in the tool configuration.
- **FR-006**: System MUST implement a "Request Human Input" tool to allow the agent to ask clarifying questions when needed.
- **FR-007**: System MUST support basic built-in tools: `code_execution`, `web_search`, and `request_human_input`.
- **FR-008**: System MUST provide a standardized interface for tools to return results (Success/Error) back to the agent.
- **FR-009**: System SHALL execute local tool scripts in the current application environment without additional isolation, assuming they are trusted components.
- **FR-010**: System MUST provide API endpoints to register, update, and remove tools, with changes persisted to the underlying JSON configuration files.
- **FR-011**: System MUST log every tool execution, including the tool name, input arguments, execution timestamp, and the full output or error message returned.
- **FR-012**: System MUST validate the tool registry files at startup and during API updates, failing immediately if the configuration is malformed or missing.
- **FR-013**: System MUST support optional parallel execution for tools specifically marked as `parallel_capable: true` in their configuration.
- **FR-014**: System MUST enforce a configurable timeout for each tool execution, defaulting to a system-wide value if not specified.
- **FR-015**: System MUST process all persistent tool registry updates via a sequential queue to ensure data integrity during concurrent API requests.
- **FR-016**: System MUST rotate `ToolExecutionLog` entries daily and retain them for 30 days.
- **FR-017**: System MUST implement a retry mechanism for transient MCP connection failures, attempting 3 retries with exponential backoff.

### Key Entities *(include if feature involves data)*

- **Tool**: Represents a unit of capability. Contains name, description, input schema, output schema, parallel capability flag, timeout value, and the execution logic (local script or MCP endpoint).
- **Tool Configuration (`tools.json`)**: A registry of locally available tools and their metadata.
- **MCP Configuration (`mcp.json`)**: A registry of external MCP servers and connection parameters.
- **Execution Context**: The environment where tools are executed, maintaining state and handling communication between the agent and tools.
- **ToolExecutionLog**: Records the history of tool calls for observability.
- **ToolResponse**: The standardized envelope for all tool execution results. Contains status (success/error), data, and optional error message.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can get answers to current event questions (requiring `web_search`) with 90% accuracy in tool selection. Accuracy is measured using a gold-standard dataset of 50 test prompts.
- **SC-002**: A new tool can be fully registered and usable by the agent in under 5 minutes by a developer via API.
- **SC-003**: Tool execution overhead (excluding the tool's internal processing time) is less than 200ms. Overhead is measured as the time delta between agent tool request and tool execution start.
- **SC-004**: 100% of tool inputs/outputs are validated against their defined schemas, preventing malformed data from reaching tools or the agent.
- **SC-005**: Agent successfully falls back to `request_human_input` when it determines it lacks sufficient information to proceed with any other tool.
- **SC-006**: 100% of tool executions are traceable via logs, enabling root-cause analysis for any tool-related failure.

