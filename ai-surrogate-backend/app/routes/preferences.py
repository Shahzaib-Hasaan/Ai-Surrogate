"""
User Preferences Routes

API endpoints for managing user preferences and personalization.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel

from app.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.services.preferences_service import preferences_service

router = APIRouter(prefix="/api/preferences", tags=["preferences"])


# Pydantic models
class PreferencesUpdate(BaseModel):
    """Model for updating preferences."""
    preferred_language: Optional[str] = None
    preferred_tone: Optional[str] = None
    conversation_style: Optional[str] = None
    response_length: Optional[str] = None
    name: Optional[str] = None
    timezone: Optional[str] = None
    custom_context: Optional[str] = None


class TopicAdd(BaseModel):
    """Model for adding a topic."""
    topic: str


@router.get("/")
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user preferences."""
    prefs = preferences_service.get_or_create_preferences(
        user_id=str(current_user.id),
        db=db
    )
    return prefs.to_dict()


@router.put("/")
async def update_preferences(
    update: PreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preferences."""
    # Filter out None values
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    
    prefs = preferences_service.update_preferences(
        user_id=str(current_user.id),
        db=db,
        **update_data
    )
    
    return {
        "message": "Preferences updated successfully",
        "preferences": prefs.to_dict()
    }


@router.post("/topics")
async def add_topic(
    topic_data: TopicAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a topic of interest."""
    prefs = preferences_service.add_topic_of_interest(
        user_id=str(current_user.id),
        topic=topic_data.topic,
        db=db
    )
    
    return {
        "message": "Topic added successfully",
        "topics": prefs.topics_of_interest
    }


@router.get("/context")
async def get_personalization_context(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalization context for AI."""
    context = preferences_service.get_personalization_context(
        user_id=str(current_user.id),
        db=db
    )
    
    return {
        "context": context
    }
