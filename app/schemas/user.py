from pydantic import BaseModel, Field


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
