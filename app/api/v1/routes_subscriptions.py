from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.sql import SessionLocal
from sqlalchemy.orm import Session
from app.api.v1.routes_auth import get_current_user
from app.schemas.customer import CreateCustomerRequest
from app.models.customer import Customer
from app.schemas.subscriptions import CreateSubscriptionsRequest, Payment
from app.models.subscription import Subscription
from app.db.mongo_job_logs import payment


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error to connect sql db",
        )
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# - POST /subscriptions → Subscribe a customer to a plan
# - POST /payments/simulate → Simulate a payment (no real gateway, just a dummy success/failure)
# - POST /payments/simulate → Simulate a payment (no real gateway, just a dummy success/failure)
# 4. When a payment simulation occurs:
#     - Store the transaction result (customer_id, plan_id, amount, timestamp, status) in a **NoSQL database** (e.g., MongoDB or Firebase Firestore).


@router.post("/payment")
async def payment_simulation(payload: Payment):
    data = payload.model_dump()
    data["customer_id"] = str(data["customer_id"])
    data["plan_id"] = str(data["plan_id"])
    await payment(data)


@router.post("/")
async def create_subscription(
    user: user_dependency, db: db_dependency, payload: CreateSubscriptionsRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    subscription = Subscription(**payload.model_dump())
    db.add(subscription)
    db.commit()

    return subscription
