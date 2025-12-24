"""
Conversation model for grouping related messages.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Conversation(Base):
    """
    Conversation model representing a chat session between user and AI.
    
    Attributes:
        id: Unique identifier (UUID)
        user_id: Foreign key to User
        title: Optional conversation title
        created_at: Timestamp of conversation creation
        updated_at: Timestamp of last update
        
    Relationships:
        user: The user who owns this conversation
        messages: All messages in this conversation
    """
    
    __tablename__ = "conversations"
    
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
    
    title = Column(
        String(200),
        nullable=True
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    user = relationship(
        "User",
        back_populates="conversations"
    )
    
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at"
    )
    
    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, user_id={self.user_id}, title={self.title})>"
