
from pydantic import BaseModel
from typing import Optional, Any, Dict, Literal

class WebSocketEvent(BaseModel):
    event: Literal['status_update', 'request_input', 'final_answer', 'error', 'user_response']
    payload: Dict[str, Any]

# Outgoing events
class StatusUpdatePayload(BaseModel):
    status: str
    thought: Optional[str] = None
    tool_call: Optional[str] = None

class RequestInputPayload(BaseModel):
    prompt: str

class FinalAnswerPayload(BaseModel):
    content: str

class ErrorPayload(BaseModel):
    message: str

# Incoming events
class UserResponsePayload(BaseModel):
    content: str
