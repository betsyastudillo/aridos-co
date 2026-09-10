from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    document_id: str
    full_name: str
    email: str
    role: str
    company_id: UUID
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    document_id: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"