from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    name: str | None = Field(default=None, max_length=160)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProfileUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=160)
    location: str | None = Field(default=None, max_length=160)
    target_roles: list[str] = Field(default_factory=list, max_length=20)
    skills: list[str] = Field(default_factory=list, max_length=100)
    years_experience: float | None = Field(default=None, ge=0, le=80)
    remote_preference: str | None = Field(default=None, pattern="^(remote|hybrid|onsite)$")


class ProfileResponse(ProfileUpdate):
    user_id: UUID
    email: EmailStr


class AlertCreate(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    location: str | None = Field(default=None, max_length=160)
    remote_type: str | None = Field(default=None, pattern="^(remote|hybrid|onsite)$")
    min_match: int | None = Field(default=None, ge=0, le=100)


class AlertResponse(AlertCreate):
    id: UUID
    enabled: bool
    created_at: datetime
