from pydantic import BaseModel, Field
from typing import Optional


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class UpdateProfile(BaseModel):
    email: Optional[str] = Field(None)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
