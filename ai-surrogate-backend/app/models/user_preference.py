"""
User Preferences Model

Stores user-specific preferences and context for personalized AI responses.
"""

from sqlalchemy import Column, String, JSON, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base


class UserPreference(Base):
    """User preferences and context storage."""
    
    __tablename__ = "user_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Preference categories
    preferred_language = Column(String(10), default="en")
    preferred_tone = Column(String(50), default="friendly")  # friendly, professional, casual
    topics_of_interest = Column(JSON, default=list)  # List of topics user talks about
    
    # Context tracking
    conversation_style = Column(String(50), default="balanced")  # concise, detailed, balanced
    response_length = Column(String(20), default="medium")  # short, medium, long
    
    # User profile
    name = Column(String(100), nullable=True)
    timezone = Column(String(50), nullable=True)
    custom_context = Column(Text, nullable=True)  # Free-form context about user
    
    # Metadata
    preferences_json = Column(JSON, default=dict)  # Additional preferences
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "preferred_language": self.preferred_language,
            "preferred_tone": self.preferred_tone,
            "topics_of_interest": self.topics_of_interest,
            "conversation_style": self.conversation_style,
            "response_length": self.response_length,
            "name": self.name,
            "timezone": self.timezone,
            "custom_context": self.custom_context,
            "preferences_json": self.preferences_json,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
