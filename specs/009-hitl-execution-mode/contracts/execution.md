# API Contract: Skill Execution

## REST Endpoints

### Start Execution
`POST /api/execution/start`

**Request**:
```json
{
  "skill_id": "9843e740-ae55-489c-9ce4-5749338343dd",
  "input": "Deploy the 'hello-world' app to production",
  "mode": "HITL",
  "config": {
    "model_id": "gemini-1.5-pro",
    "max_steps": 10
  }
}
```

**Response** (201 Created):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "RUNNING"
}
```

### Get Session Status
`GET /api/execution/sessions/{session_id}`

**Response**:
```json
{
  "session_id": "...",
  "status": "PAUSED",
  "history": [...]
}
```

## WebSocket Protocol
`WS /ws/execution/{session_id}`

### Server -> Client (Events)

#### `status_update`
Sent whenever the agent changes state or performs a step.
```json
{
  "event": "status_update",
  "payload": {
    "status": "THINKING",
    "thought": "I need to check the current folder contents...",
    "tool_call": "ls"
  }
}
```

#### `request_input`
Sent when the agent is waiting for user feedback.
```json
{
  "event": "request_input",
  "payload": {
    "prompt": "Which deployment region should I use?"
  }
}
```

#### `final_answer`
Sent when the execution completes successfully.
```json
{
  "event": "final_answer",
  "payload": {
    "content": "Deployment successful in us-central1."
  }
}
```

### Client -> Server (Events)

#### `user_response`
Sent to resume a `PAUSED` session.
```json
{
  "event": "user_response",
  "payload": {
    "content": "us-east1"
  }
}
```