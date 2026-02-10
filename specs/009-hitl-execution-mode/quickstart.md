# Quickstart: Human-in-the-Loop (HITL) Execution Mode

## 1. Starting a Session
Send a `POST` request to `/api/execution/start` with the target `skill_id` and set `"mode": "HITL"`.

## 2. Connecting to the Stream
Connect to the WebSocket at `ws://localhost:8000/ws/execution/{session_id}`. You will receive real-time updates of the agent's reasoning.

## 3. Handling Input Requests
When you receive a `request_input` event on the WebSocket:
1. The UI should display the `prompt` to the user.
2. The UI should block further actions until the user provides a response.

## 4. Resuming the Agent
Send a `user_response` event back through the WebSocket:
```json
{
  "event": "user_response",
  "payload": { "content": "Your answer here" }
}
```
The agent will automatically transition from `PAUSED` back to `RUNNING` and process the input.

## 5. Monitoring
Use the `GET /api/execution/sessions/{session_id}` endpoint to fetch the full conversation history for audit or persistence purposes.