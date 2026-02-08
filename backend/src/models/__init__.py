from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Complexity(str, Enum):
    SIMPLE = "SIMPLE"
    COMPLEX = "COMPLEX"

class ExecutionOutcome(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    NO_MATCH = "NO_MATCH"

class Skill(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    metadata_path: str
    code_path: str
    complexity: Complexity
    version: str
    source_url: str
    last_synced: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)

class ReACTStep(BaseModel):
    thought: str
    action: Optional[str] = None
    observation: Optional[str] = None

class ExecutionLog(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    skill_id: Optional[UUID] = None
    query: str
    confidence_score: Optional[float] = None
    steps: List[ReACTStep] = []
    outcome: ExecutionOutcome
    model_used: Optional[str] = None
    duration: float
    timestamp: datetime = Field(default_factory=datetime.now)

class SkillDocumentation(BaseModel):
    skill_id: UUID
    content: str
    file_name: str

class SkillRegistry(BaseModel):
    skills: List[Skill] = []
    last_updated: datetime = Field(default_factory=datetime.now)

from .registration import (
    RiskCategory,
    RiskSeverity,
    RiskFinding,
    SafetyStatus,
    Judgment,
    BatchStatus,
    RegistrationQueueItem,
    RegistrationBatch,
    GitHubDeepLink
)

from .execution import (
    ExecutionMode,
    ExecutionStatus,
    MessageRole,
    ExecutionMessage,
    ExecutionSession
)
