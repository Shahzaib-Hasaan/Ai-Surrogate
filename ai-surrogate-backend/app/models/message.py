"""
Message model for storing chat messages.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Message(Base):
    """
    Message model representing individual chat messages.
    
    Attributes:
        id: Unique identifier (UUID)
        user_id: Foreign key to User
        conversation_id: Foreign key to Conversation
        content: The message text content
        is_from_user: True if message is from user, False if from AI
        created_at: Timestamp of message creation
        
    Relationships:
        user: The user who sent/received this message
        conversation: The conversation this message belongs to
    """
    
    __tablename__ = "messages"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    content = Column(
        Text,
        nullable=False
    )
    
    is_from_user = Column(
        Boolean,
        nullable=False
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True  # Index for sorting by time
    )
    
    # Relationships
    user = relationship(
        "User",
        back_populates="messages"
    )
    
    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )
    
    def __repr__(self) -> str:
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Message(id={self.id}, is_from_user={self.is_from_user}, content='{content_preview}')>"
