from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.sql import SessionLocal
from sqlalchemy.orm import Session
from app.api.v1.routes_auth import get_current_user
from app.schemas.customer import CreateCustomerRequest
from app.models.customer import Customer


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


# - POST /customers → Create a new customer
# - GET /customers → List all customers


@router.post("/")
async def create_customer(
    user: user_dependency, db: db_dependency, payload: CreateCustomerRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/")
async def list_customers(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    customers = db.query(Customer).all()
    return customers
