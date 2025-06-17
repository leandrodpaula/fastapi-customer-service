# src/interfaces/api/schemas.py
import uuid
from pydantic import BaseModel, EmailStr, Field

class CustomerBase(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="johndoe@example.com")

class CustomerCreateRequest(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: uuid.UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")

    class Config:
        orm_mode = True # For compatibility if returning ORM models directly, good practice
