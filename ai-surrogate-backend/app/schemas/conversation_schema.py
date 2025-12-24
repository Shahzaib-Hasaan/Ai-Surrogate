"""
Conversation-related Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.message_schema import MessageResponse


class ConversationCreate(BaseModel):
    """Schema for creating a new conversation."""
    
    title: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Conversation title (optional)",
        examples=["My Chat with AI"]
    )


class ConversationResponse(BaseModel):
    """Schema for conversation data in responses."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(..., description="Conversation unique identifier")
    title: Optional[str] = Field(None, description="Conversation title")
    created_at: datetime = Field(..., description="Conversation creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    user_id: UUID = Field(..., description="User who owns this conversation")


class ConversationWithMessages(ConversationResponse):
    """Schema for conversation with its messages."""
    
    messages: List[MessageResponse] = Field(
        default_factory=list,
        description="List of messages in this conversation"
    )
