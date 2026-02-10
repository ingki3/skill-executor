# Feature Specification: Human-in-the-Loop (HITL) Execution Mode

**Feature Branch**: `009-hitl-execution-mode`  
**Created**: 2026-02-08  
**Status**: Draft  
**Input**: User description: "'/Users/hyungjoolee/dev/skill-executor/prd.md'의 변경 내용을 보고 작업 준비해줘."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interactive Skill Execution (HITL Enabled) (Priority: P1)

As a user, I want the agent to pause and ask me for clarification when it encounters an ambiguous step during skill execution, so that I can provide the necessary details to ensure the task is completed correctly.

**Why this priority**: This is the core functionality of the "Human-in-the-Loop" feature, allowing for higher success rates in complex tasks.

**Independent Test**: Can be tested by running a "Complex" skill that requires user input (e.g., "Ask me for a favorite color then print it"), verifying the agent pauses, and checking that it resumes correctly after receiving the input.

**Acceptance Scenarios**:

1. **Given** a registered skill that requires user input, **When** the user executes the skill with HITL mode ENABLED, **Then** the system should display a prompt asking for the missing information and pause execution.
2. **Given** a paused execution session, **When** the user provides the requested information, **Then** the agent should resume execution and complete the task using the provided data.

---

### User Story 2 - Autonomous Skill Execution (HITL Disabled) (Priority: P2)

As a user, I want to run skills fully autonomously without manual intervention, so that I can automate repetitive tasks without monitoring the progress.

**Why this priority**: Enables automation and hands-off operation, which is a key goal for agentic systems.

**Independent Test**: Can be tested by running a skill with HITL mode DISABLED and verifying it either completes using defaults or fails gracefully without ever pausing for user input.

**Acceptance Scenarios**:

1. **Given** any skill, **When** the user executes it with HITL mode DISABLED, **Then** the system should run the execution loop until completion or until the maximum iteration limit is reached without pausing.
2. **Given** an ambiguous situation in autonomous mode, **When** the agent hits a roadblock, **Then** it should apply fallback strategies (like using default values or failing with a clear error message) rather than waiting for input.

---

### User Story 3 - Session Context Persistence (Priority: P3)

As a user, I want my conversation and execution context to be preserved during an active session, even if I momentarily navigate away, so that I don't lose progress on long-running tasks.

**Why this priority**: Ensures a smooth user experience for complex, multi-step tasks.

**Independent Test**: Can be tested by starting a HITL session, navigating to another page in the Admin Dashboard, and returning to the execution view to confirm the session state is still active and the history is preserved.

**Acceptance Scenarios**:

1. **Given** an active execution session, **When** the user navigates away and returns within the timeout period, **Then** the conversation history and current execution state should be restored.
2. **Given** an inactive session, **When** the session exceeds the 30-minute timeout, **Then** the system should automatically clean up the resources and terminate the session.

---

### Edge Cases

- **Max Iteration Limit**: How does the system handle an autonomous agent that keeps looping without reaching a final answer? (System MUST terminate after 10 steps).
- **Network Disconnection**: What happens if the UI loses connection to the backend during a paused session? (Session state MUST persist on the server for the timeout duration).
- **Ambiguous Skill Metadata**: What if a skill is marked "Simple" but tries to use HITL? (Simple skills should generally not support HITL, or HITL should be ignored for them as they use direct execution).

## Clarifications

### Session 2026-02-08
- Q: How many concurrent active execution sessions should the system support? → A: Limited concurrent sessions (max 5)
- Q: What types of input should the HITL mode support for human feedback? → A: Text-only input
- Q: What should be the system behavior when a session exceeds the 30-minute timeout? → A: Terminate and clean up resources
- Q: How much of the agent's internal reasoning process should be visible to the user? → A: Full reasoning visible (Chain of Thought)
- Q: Should users be able to re-execute or "rewind" a completed session? → A: View history only; must start new session

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a toggle/option in the execution interface to enable or disable "Human-in-the-Loop" mode before starting a skill.
- **FR-002**: System MUST maintain persistent session storage (using local memory or JSON serialization) to retain conversation history and agent state across browser refreshes.
- **FR-003**: System MUST use a conversation memory system to retain dialogue history within a session.
- **FR-004**: In HITL mode, the agent MUST be able to emit a "Request for Input" signal and display its full **Execution Reasoning** (thoughts and tool calls) to the user before pausing.
- **FR-005**: System MUST allow the user to submit text-only input to a paused session to resume execution.
- **FR-006**: System MUST automatically terminate sessions and reclaim all resources after a 30-minute period of inactivity.
- **FR-007**: In Autonomous mode, the system MUST enforce a maximum of 10 execution steps to prevent infinite execution loops.
- **FR-008**: System MUST support up to 5 concurrent active execution sessions. If the limit is reached, new execution requests MUST be rejected with a "Maximum concurrent sessions reached" error.
- **FR-009**: System MUST allow users to view the history of completed sessions, but re-execution MUST require a new session.

### Key Entities *(include if feature involves data)*

- **Execution Session**: Represents an active or paused skill execution. Contains: `session_id`, `skill_id`, `mode` (HITL/Autonomous), `status` (Running/Paused/Completed/Failed), `history` (Conversation log), `last_active_at`.
- **Conversation History**: A collection of messages between the user and the agent within a session.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of HITL-enabled sessions successfully resume and incorporate user input into the agent's logic.
- **SC-002**: Autonomous executions never exceed 10 steps, terminating with either a result or a graceful failure.
- **SC-003**: Session state and history are preserved with 100% accuracy during the 30-minute window, even if the user refreshes the browser.
- **SC-004**: System successfully cleans up 100% of expired sessions (older than 30 minutes) to prevent memory leaks.