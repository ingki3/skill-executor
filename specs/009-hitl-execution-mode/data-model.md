# Data Model: Human-in-the-Loop (HITL) Execution Mode

## Entities

### ExecutionSession
Represents a single execution run of a skill.

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | UUID | Unique identifier |
| `skill_id` | String | Reference to the registered skill |
| `mode` | Enum | `HITL` or `AUTONOMOUS` |
| `status` | Enum | `RUNNING`, `PAUSED`, `COMPLETED`, `FAILED` |
| `config` | Dict | Execution parameters (e.g., model_id, max_steps) |
| `created_at` | DateTime | Session start time |
| `last_active` | DateTime | Last interaction time |

### ExecutionMessage
A single interaction within an execution session.

| Field | Type | Description |
|-------|------|-------------|
| `message_id` | UUID | Unique identifier |
| `session_id` | UUID | FK to ExecutionSession |
| `role` | Enum | `HUMAN`, `AI`, `SYSTEM`, `TOOL` |
| `content` | String | The message content (text) |
| `metadata` | Dict | Reasoning steps, tool names, etc. |
| `timestamp` | DateTime | Message creation time |

## Relationships
- **Skill (1) <--- (N) ExecutionSession**: A skill can be run many times.
- **ExecutionSession (1) <--- (N) ExecutionMessage**: A session tracks a stream of messages.

## State Transitions
1. `CREATED` -> `RUNNING`: Start command received.
2. `RUNNING` -> `PAUSED`: `RequestInputTool` invoked (HITL only).
3. `PAUSED` -> `RUNNING`: User input received.
4. `RUNNING` -> `COMPLETED`: Agent reaches final answer.
5. `RUNNING` -> `FAILED`: Max steps reached or runtime error.