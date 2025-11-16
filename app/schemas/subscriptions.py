from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class CreateSubscriptionsRequest(BaseModel):
    customer_id: UUID
    plan_id: UUID
    start_date: datetime
    end_date: datetime
    status: str


# customer_id, plan_id, amount, timestamp, status


class Payment(BaseModel):
    customer_id: UUID
    plan_id: UUID
    amount: float
    timestamp: datetime
    status: str


# customer_id
# plan_id
# start_date
# end_date
# status
