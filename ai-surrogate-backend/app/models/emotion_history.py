"""
Emotion History Model

Tracks user emotional patterns over time.
"""

from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class EmotionHistory(Base):
    """Track emotional patterns in conversations."""
    
    __tablename__ = "emotion_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=False)
    
    # Detected emotion
    emotion = Column(String(50), nullable=False)  # happy, sad, angry, etc.
    confidence = Column(Float, default=0.8)  # How confident we are
    intensity = Column(Float, default=0.5)  # How intense the emotion is
    
    # Context
    user_message = Column(String, nullable=False)
    ai_response = Column(String, nullable=False)
    
    # Metadata
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="emotion_history")
    conversation = relationship("Conversation")
    message = relationship("Message")
    
    def __repr__(self):
        return f"<EmotionHistory {self.emotion} ({self.confidence:.0%})>"
