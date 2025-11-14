from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class JobBase(BaseModel):
    agent_id: UUID
    input_text: str


class JobCreate(JobBase):
    """Payload to create a new Job"""

    pass


class JobResponse(JobBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pydantic v2 with SQLAlchemy


class JobStatusUpdate(BaseModel):
    status: str  # "pending" | "running" | "completed" | "failed"
