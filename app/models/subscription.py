from typing import List, Optional, Dict, Any, Text
from app.db.sql import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.sql import Base


# SubscriptionPlan → id, name, price, billing_cycle (e.g., monthly, yearly)
class SubscriptionPlan(Base):
    __tablename__ = "subscription_plan"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True)
    price = Column(Integer)
    billing_cycle = Column(String)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "price": self.price,
            "billing_cycle": self.billing_cycle,
        }


# Subscription → id, customer_id, plan_id, start_date, end_date, status
class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # relations
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    plan_id = Column(
        UUID(as_uuid=True), ForeignKey("subscription_plan.id"), nullable=False
    )

    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), onupdate=func.now())

    # status: pending, running, completed, failed
    status = Column(String(20), nullable=False, default="pending")

    def to_dict(self):
        return {
            "id": str(self.id),
            "customer_id": self.customer_id,
            "plan_id": self.plan_id,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
