
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

class ExecutionMode(str, Enum):
    HITL = "HITL"
    AUTONOMOUS = "AUTONOMOUS"

class ExecutionStatus(str, Enum):
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    THINKING = "THINKING"
    TOOL_CALL = "TOOL_CALL"

class MessageRole(str, Enum):
    HUMAN = "HUMAN"
    AI = "AI"
    SYSTEM = "SYSTEM"
    TOOL = "TOOL"

class ExecutionMessage(BaseModel):
    message_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    role: MessageRole
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)

class ExecutionSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    skill_id: str
    mode: ExecutionMode
    status: ExecutionStatus
    config: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    last_active: datetime = Field(default_factory=datetime.now)
    history: List[ExecutionMessage] = Field(default_factory=list)
