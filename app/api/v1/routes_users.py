from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.sql import SessionLocal
from sqlalchemy.orm import Session
from app.models.user import Users
from app.schemas.user import UserVerification, UpdateProfile
from app.api.v1.routes_auth import get_current_user
from passlib.context import CryptContext


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
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/profile", status_code=status.HTTP_200_OK)
async def update_profile(
    user: user_dependency, db: db_dependency, payload: UpdateProfile
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    user_model = db.query(Users).filter(Users.id == user["id"]).first()
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user_model, field, value)

    db.commit()
    db.refresh(user_model)

    # Return user data without sensitive information
    return {
        "message": "Profile updated successfully",
        "user": {
            "id": str(user_model.id),
            "email": user_model.email,
            "username": user_model.username,
            "first_name": user_model.first_name,
            "last_name": user_model.last_name,
            "role": user_model.role,
            "phone_number": user_model.phone_number,
            "is_active": user_model.is_active
        }
    }
