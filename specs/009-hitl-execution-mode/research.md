# Research: Human-in-the-Loop (HITL) Execution Mode

## Phase 0: Research & Decisions

### 1. Interruptible Agent Loop
**Decision**: Implement a custom `InterruptTool` (or `RequestInputTool`) within the LangChain Agent.
**Rationale**: 
- When the agent decides it needs input, it calls the tool.
- The tool raises a `HumanInterrupt` exception.
- The `ExecutionService` catches this, persists the `AgentState` (messages + memory), and marks the session as `PAUSED`.
- Resuming simply involves re-triggering the loop with the user's response as the output of that tool.
**Alternatives Considered**: 
- Long-running async events: Harder to manage across multiple concurrent sessions and fragile to timeouts.

### 2. Real-time Communication
**Decision**: **FastAPI WebSockets**.
**Rationale**: 
- Bi-directional: Necessary for the agent to "push" thoughts and for the user to "push" input.
- Low Latency: Critical for a "feeling" of interactivity while the agent is thinking.
- Streaming: Supports token-by-token streaming of reasoning steps.
**Alternatives Considered**: 
- Polling: High overhead and slow.
- SSE (Server-Sent Events): One-way only; would need separate REST calls for user input.

### 3. Session Recovery & Persistence
**Decision**: **In-memory Registry with JSON serialization**.
**Rationale**: 
- Given the single-instance Docker deployment, in-memory is fastest.
- We will serialize the session metadata and message history to `.skill-executor-data/sessions.json` periodically to allow some level of recovery.
- Full agent object state (Python instance) won't survive a restart, but the message history can re-instantiate a new agent with the same context.
**Alternatives Considered**: 
- Redis: Great, but adds a dependency for the initial MVP. 
- SQLAlchemy/Postgres: Overkill for transient execution state.

## Summary of Tech Choices
- **Engine**: LangChain `AgentExecutor` with custom callbacks.
- **Communication**: FastAPI WebSocket endpoints.
- **Memory**: `ConversationBufferWindowMemory` (k=10).