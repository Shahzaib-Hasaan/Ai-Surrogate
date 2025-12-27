"""
User model for authentication and user management.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """
    User model representing registered users in the system.
    
    Attributes:
        id: Unique identifier (UUID)
        email: User's email address (unique)
        username: User's display name (unique)
        hashed_password: Bcrypt hashed password
        created_at: Timestamp of account creation
        updated_at: Timestamp of last update
        is_active: Whether the account is active
        
    Relationships:
        conversations: All conversations belonging to this user
        messages: All messages sent by this user
    """
    
    __tablename__ = "users"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    
    username = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )
    
    hashed_password = Column(
        String(255),
        nullable=False
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
    
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )
    
    # Relationships
    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    messages = relationship(
        "Message",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    emotion_history = relationship(
        "EmotionHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
