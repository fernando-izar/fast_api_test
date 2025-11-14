from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    model_name: str
    instructions: Optional[str] = None


class AgentCreate(AgentBase):
    """Used when creating an agent"""

    pass


class AgentResponse(AgentBase):
    id: UUID
    owner_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
