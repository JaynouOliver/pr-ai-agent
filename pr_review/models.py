from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

# Input Models
class PRRequest(BaseModel):
    repo_url: str
    pr_number: int

# Analysis Models
class Issue(BaseModel):
    type: str
    line: int
    description: str
    suggestion: str

class File(BaseModel):
    name: str
    issues: List[Issue]

class Summary(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int

class AnalysisResult(BaseModel):
    files: List[File]
    summary: Summary

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Response Models
class TaskResponse(BaseModel):
    task_id: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: TaskStatus

class AnalysisTaskResponse(BaseModel):
    task_id: str
    result: Optional[AnalysisResult] = None
    error: Optional[str] = None
