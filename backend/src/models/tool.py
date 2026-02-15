from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime

class ToolType(str, Enum):
    LOCAL = "local"
    MCP = "mcp"

class ToolDefinition(BaseModel):
    name: str = Field(..., description="Unique identifier for the tool")
    description: str = Field(..., description="Natural language description for the LLM")
    type: ToolType
    input_schema: Dict[str, Any] = Field(..., description="JSON Schema for inputs")
    output_schema: Optional[Dict[str, Any]] = Field(None, description="JSON Schema for outputs")
    parallel_capable: bool = False
    timeout: Optional[int] = Field(30, description="Execution timeout in seconds")
    config: Dict[str, Any] = Field(default_factory=dict, description="Type-specific configuration")

class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class ToolResponse(BaseModel):
    status: ExecutionStatus
    data: Optional[Any] = None
    message: Optional[str] = None
    execution_id: Optional[UUID] = None

class ToolExecutionLog(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now)
    tool_name: str
    input_args: Dict[str, Any]
    output: Optional[Any] = None
    duration_ms: int = 0
    status: ExecutionStatus
    error_message: Optional[str] = None
