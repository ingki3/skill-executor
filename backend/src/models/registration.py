from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

class RiskCategory(str, Enum):
    PII = "PII"
    MALICIOUS_CODE = "MALICIOUS_CODE"
    DANGEROUS_OP = "DANGEROUS_OP"
    OTHER = "OTHER"

class RiskSeverity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class RiskFinding(BaseModel):
    category: RiskCategory
    detail: str
    severity: RiskSeverity

class SafetyStatus(str, Enum):
    SCANNING = "SCANNING"
    SAFE = "SAFE"
    RISKY = "RISKY"
    FAILED = "FAILED"

class Judgment(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class BatchStatus(str, Enum):
    SCANNING = "SCANNING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class RegistrationQueueItem(BaseModel):
    path: str
    name: str
    safety_status: SafetyStatus = SafetyStatus.SCANNING
    judgment: Judgment = Judgment.PENDING
    risk_findings: List[RiskFinding] = []
    code_content: Optional[str] = None
    error_message: Optional[str] = None

class RegistrationBatch(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    repo_url: str
    status: BatchStatus = BatchStatus.SCANNING
    items: List[RegistrationQueueItem] = []
    created_at: datetime = Field(default_factory=datetime.now)

class GitHubDeepLink(BaseModel):
    is_github: bool
    is_deep_link: bool
    repo_url: str
    branch: Optional[str] = None
    sub_path: Optional[str] = None
