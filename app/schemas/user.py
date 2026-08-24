from pydantic import BaseModel, Field, ConfigDict, EmailStr
from app.models.user import UserRole
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr = Field(description="Email of the user")


class UserCreate(UserBase):
    password: str = Field(description="user hashed password")


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description="Unique identifier of the user")
    role: UserRole = Field(default=UserRole.CUSTOMER, description="Role of the user")


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str = Field(description="JWT Access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    email: Optional[str] = None
