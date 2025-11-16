from typing import List, Optional, Dict, Any
from app.db.sql import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True)
    name = Column(String, unique=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),  # Convert UUID to string for JSON serialization
            "email": self.email,
            "name": self.name,
        }
