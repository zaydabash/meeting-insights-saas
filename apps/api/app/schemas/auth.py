from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.schemas.user import UserResponse
from app.schemas.organization import OrganizationResponse


class RegisterRequest(BaseModel):
    org_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    user: UserResponse
    org: OrganizationResponse

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

