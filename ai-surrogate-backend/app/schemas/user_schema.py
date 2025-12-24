"""
User-related Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    """Schema for user registration request."""
    
    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"]
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="User's display name",
        examples=["john_doe"]
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User's password (min 8 characters)",
        examples=["SecurePass123!"]
    )


class UserLogin(BaseModel):
    """Schema for user login request."""
    
    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"]
    )
    password: str = Field(
        ...,
        description="User's password",
        examples=["SecurePass123!"]
    )


class UserResponse(BaseModel):
    """Schema for user data in responses."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="User's unique identifier")
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's display name")
    created_at: datetime = Field(..., description="Account creation timestamp")
    is_active: bool = Field(..., description="Whether the account is active")


class Token(BaseModel):
    """Schema for JWT token response."""
    
    access_token: str = Field(
        ...,
        description="JWT access token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    token_type: str = Field(
        default="bearer",
        description="Token type",
        examples=["bearer"]
    )


class TokenData(BaseModel):
    """Schema for decoded JWT token data."""
    
    user_id: Optional[UUID] = None
    email: Optional[str] = None
