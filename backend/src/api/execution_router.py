import json
import asyncio
from typing import Dict, List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Body
from src.models import ExecutionSession, ExecutionMode, ExecutionStatus
from src.services.execution import execution_service
from src.services.session_registry import session_registry
from .websocket_schemas import WebSocketEvent, StatusUpdatePayload, RequestInputPayload, FinalAnswerPayload, ErrorPayload

router = APIRouter(prefix="/execution", tags=["execution"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID, List[WebSocket]] = {}

    async def connect(self, session_id: UUID, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, session_id: UUID, websocket: WebSocket):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, session_id: UUID, event: WebSocketEvent):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_text(event.model_dump_json())

    async def broadcast_status(self, session_id: UUID, status: str, thought: str = None, tool_call: str = None):
        event = WebSocketEvent(
            event="status_update",
            payload=StatusUpdatePayload(status=status, thought=thought, tool_call=tool_call).model_dump()
        )
        await self.broadcast(session_id, event)

    async def broadcast_input_request(self, session_id: UUID, prompt: str):
        event = WebSocketEvent(
            event="request_input",
            payload=RequestInputPayload(prompt=prompt).model_dump()
        )
        await self.broadcast(session_id, event)

    async def broadcast_final(self, session_id: UUID, content: str):
        event = WebSocketEvent(
            event="final_answer",
            payload=FinalAnswerPayload(content=content).model_dump()
        )
        await self.broadcast(session_id, event)

    async def broadcast_error(self, session_id: UUID, message: str):
        event = WebSocketEvent(
            event="error",
            payload=ErrorPayload(message=message).model_dump()
        )
        await self.broadcast(session_id, event)

manager = ConnectionManager()
execution_service.set_websocket_manager(manager)

@router.post("/start", response_model=ExecutionSession, status_code=201)
async def start_execution(
    skill_id: str = Body(...),
    input: str = Body(...),
    mode: ExecutionMode = Body(...),
    config: Optional[dict] = Body(default={})
):
    try:
        # FR-009: Support up to 5 concurrent active sessions
        active_sessions = session_registry.list_active_sessions()
        if len(active_sessions) >= 5:
            # FR-008: Reject with descriptive error
            raise HTTPException(status_code=429, detail="Maximum concurrent sessions reached")

        session = await execution_service.start_session(skill_id, input, mode, config)
        
        # Trigger execution (non-blocking)
        # Note: In US1, this will start the loop
        # We pass the manager to execution_service in the future
        await execution_service.run_session(session.session_id)
        
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}", response_model=ExecutionSession)
async def get_session(session_id: UUID):
    session = session_registry.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/sessions/clear")
async def clear_all_sessions():
    """Clear all sessions from memory and disk (Test helper)."""
    session_registry._sessions.clear()
    import shutil
    shutil.rmtree(session_registry.storage_dir, ignore_errors=True)
    session_registry.storage_dir.mkdir(parents=True, exist_ok=True)
    return {"message": "All sessions cleared"}

@router.post("/sessions/{session_id}/resume")
async def resume_execution(session_id: UUID, user_input: str = Body(embed=True)):
    """Resume a paused execution session via REST (Alternative to WS)."""
    session = session_registry.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status != ExecutionStatus.PAUSED:
        raise HTTPException(status_code=400, detail="Session is not in PAUSED state")

    from src.models import ExecutionMessage, MessageRole
    user_msg = ExecutionMessage(
        session_id=session_id,
        role=MessageRole.HUMAN,
        content=user_input
    )
    session_registry.add_message(session_id, user_msg)
    
    # Resume execution loop
    await execution_service.run_session(session_id, resume_input=user_input)
    return {"status": "resumed"}

@router.post("/prompts/reload")
async def reload_prompts():
    """Force reload all prompt templates from disk."""
    from src.core.prompt_loader import prompt_loader
    prompt_loader.reload()
    return {"status": "success", "message": "Prompt cache cleared"}

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: UUID):
    await manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            event_data = json.loads(data)
            
            if event_data.get("event") == "user_response":
                content = event_data.get("payload", {}).get("content")
                if content:
                    # T005: Add human message to history
                    from src.models import ExecutionMessage, MessageRole
                    user_msg = ExecutionMessage(
                        session_id=session_id,
                        role=MessageRole.HUMAN,
                        content=content
                    )
                    session_registry.add_message(session_id, user_msg)
                    
                    # Resume execution loop
                    # In a real LangChain flow, we would push this into the queue
                    # For verification, we trigger the loop again
                    asyncio.create_task(execution_service.run_session(session_id, resume_input=content))
                    
    except WebSocketDisconnect:
        manager.disconnect(session_id, websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(session_id, websocket)