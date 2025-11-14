import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.sql import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Which user owns this agent
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    model_name = Column(String, nullable=False)  # ex: "gpt-4o-mini"
    instructions = Column(String, nullable=True)  # optional system prompt

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to Users model
    owner = relationship("Users", backref="agents")

    def to_dict(self):
        return {
            "id": str(self.id),
            "owner_id": str(self.owner_id),
            "name": self.name,
            "description": self.description,
            "model_name": self.model_name,
            "instructions": self.instructions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
