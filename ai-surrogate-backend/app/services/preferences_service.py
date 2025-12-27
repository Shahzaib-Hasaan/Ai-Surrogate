"""
User Preferences Service

Manages user preferences and personalization settings.
"""

from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from app.models.user_preference import UserPreference
import logging

logger = logging.getLogger(__name__)


class PreferencesService:
    """Service for managing user preferences."""
    
    @staticmethod
    def get_or_create_preferences(user_id: str, db: Session) -> UserPreference:
        """Get user preferences or create default ones."""
        prefs = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if not prefs:
            prefs = UserPreference(user_id=user_id)
            db.add(prefs)
            db.commit()
            db.refresh(prefs)
            logger.info(f"Created default preferences for user {user_id}")
        
        return prefs
    
    @staticmethod
    def update_preferences(
        user_id: str,
        db: Session,
        **kwargs
    ) -> UserPreference:
        """Update user preferences."""
        prefs = PreferencesService.get_or_create_preferences(user_id, db)
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)
        
        db.commit()
        db.refresh(prefs)
        logger.info(f"Updated preferences for user {user_id}")
        
        return prefs
    
    @staticmethod
    def add_topic_of_interest(
        user_id: str,
        topic: str,
        db: Session
    ) -> UserPreference:
        """Add a topic to user's interests."""
        prefs = PreferencesService.get_or_create_preferences(user_id, db)
        
        if not prefs.topics_of_interest:
            prefs.topics_of_interest = []
        
        if topic not in prefs.topics_of_interest:
            prefs.topics_of_interest.append(topic)
            db.commit()
            db.refresh(prefs)
            logger.info(f"Added topic '{topic}' for user {user_id}")
        
        return prefs
    
    @staticmethod
    def get_personalization_context(user_id: str, db: Session) -> str:
        """Get personalization context for AI prompts."""
        prefs = PreferencesService.get_or_create_preferences(user_id, db)
        
        context = []
        
        if prefs.name:
            context.append(f"User's name is {prefs.name}.")
        
        if prefs.preferred_tone:
            context.append(f"Respond in a {prefs.preferred_tone} tone.")
        
        if prefs.conversation_style:
            context.append(f"Keep responses {prefs.conversation_style}.")
        
        if prefs.topics_of_interest:
            topics = ", ".join(prefs.topics_of_interest[:5])
            context.append(f"User is interested in: {topics}.")
        
        if prefs.custom_context:
            context.append(prefs.custom_context)
        
        return " ".join(context) if context else ""


# Global instance
preferences_service = PreferencesService()
