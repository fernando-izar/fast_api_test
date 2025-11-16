from pydantic import BaseModel, Field
from typing import Optional


class CreateCustomerRequest(BaseModel):
    name: str
    email: str
