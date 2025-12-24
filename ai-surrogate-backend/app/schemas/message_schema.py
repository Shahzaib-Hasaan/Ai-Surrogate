"""
Message-related Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class MessageCreate(BaseModel):
    """Schema for creating a new message."""
    
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Message content",
        examples=["Hello, how are you?"]
    )
    conversation_id: Optional[UUID] = Field(
        default=None,
        description="Conversation ID (optional, will create new if not provided)",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )


class MessageResponse(BaseModel):
    """Schema for message data in responses."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Message unique identifier")
    content: str = Field(..., description="Message content")
    is_from_user: bool = Field(..., description="True if from user, False if from AI")
    created_at: datetime = Field(..., description="Message creation timestamp")
    conversation_id: UUID = Field(..., description="Conversation this message belongs to")
