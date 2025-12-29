"""
Mood Entry Model

Tracks user's manual mood check-ins (separate from auto-detected emotions).
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class MoodEntry(Base):
    """Track user's self-reported mood check-ins."""
    
    __tablename__ = "mood_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Mood data
    mood = Column(String(50), nullable=False)  # happy, neutral, sad, frustrated, grateful
    intensity = Column(Integer, default=3)  # 1-5 scale
    note = Column(Text, nullable=True)  # Optional user note
    
    # Source tracking
    source = Column(String(20), default='user_logged')  # Always 'user_logged' for this model
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="mood_entries")
    
    def __repr__(self):
        return f"<MoodEntry {self.mood} (intensity: {self.intensity})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": str(self.id),
            "mood": self.mood,
            "intensity": self.intensity,
            "note": self.note,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
