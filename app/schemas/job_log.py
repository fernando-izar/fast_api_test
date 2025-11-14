from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class LogMessage(BaseModel):
    role: str  # "user" ou "agent"
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobLogCreate(BaseModel):
    job_id: UUID
    messages: List[LogMessage]


class JobLogResponse(BaseModel):
    job_id: UUID
    messages: List[LogMessage]

    class Config:
        from_attributes = True
