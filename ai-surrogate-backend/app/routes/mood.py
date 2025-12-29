"""
Mood Tracking Routes

API endpoints for mood tracking and history.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import User
from app.routes.auth import get_current_user
from app.services.mood_service import MoodService


router = APIRouter(prefix="/api/mood", tags=["mood"])


# Request/Response Models
class MoodTrackRequest(BaseModel):
    """Request model for tracking mood."""
    mood: str = Field(..., description="Mood type: happy, neutral, sad, frustrated, grateful")
    intensity: int = Field(3, ge=1, le=5, description="Intensity level 1-5")
    note: Optional[str] = Field(None, description="Optional note")


class MoodEntryResponse(BaseModel):
    """Response model for mood entry."""
    id: str
    mood: str
    intensity: int
    note: Optional[str]
    source: str
    created_at: str


@router.post("", response_model=MoodEntryResponse, status_code=status.HTTP_201_CREATED)
async def track_mood(
    request: MoodTrackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Track user's current mood.
    
    **Mood types:**
    - happy: 😊
    - neutral: 😐
    - sad: 😢
    - frustrated: 😠
    - grateful: 😌
    """
    # Validate mood type
    valid_moods = ['happy', 'neutral', 'sad', 'frustrated', 'grateful']
    if request.mood.lower() not in valid_moods:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid mood. Must be one of: {', '.join(valid_moods)}"
        )
    
    # Track mood
    mood_entry = MoodService.track_mood(
        db=db,
        user_id=str(current_user.id),
        mood=request.mood,
        intensity=request.intensity,
        note=request.note
    )
    
    return mood_entry.to_dict()


@router.get("/history")
async def get_mood_history(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's mood history for the last N days.
    
    **Query Parameters:**
    - days: Number of days to look back (default: 7)
    """
    mood_entries = MoodService.get_mood_history(
        db=db,
        user_id=str(current_user.id),
        days=days
    )
    
    return {
        "mood_entries": [entry.to_dict() for entry in mood_entries],
        "total": len(mood_entries),
        "period_days": days
    }


@router.get("/stats")
async def get_mood_stats(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get mood statistics.
    
    **Query Parameters:**
    - days: Number of days to analyze (default: 7)
    
    **Returns:**
    - total_checkins: Total number of mood check-ins
    - average_intensity: Average intensity (1-5)
    - distribution: Mood distribution with percentages
    """
    stats = MoodService.get_mood_stats(
        db=db,
        user_id=str(current_user.id),
        days=days
    )
    
    return stats


@router.get("/timeline")
async def get_mood_timeline(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get mood timeline data for charts.
    
    **Query Parameters:**
    - days: Number of days (default: 7)
    
    **Returns:**
    Daily mood averages for chart visualization.
    """
    timeline = MoodService.get_mood_timeline(
        db=db,
        user_id=str(current_user.id),
        days=days
    )
    
    return {
        "timeline": timeline,
        "period_days": days
    }
