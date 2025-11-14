from typing import List, Optional, Dict, Any
from app.db.sql import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),  # Convert UUID to string for JSON serialization
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
            "role": self.role,
            "phone_number": self.phone_number,
        }
