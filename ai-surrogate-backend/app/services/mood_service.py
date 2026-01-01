"""
Mood Service

Handles mood tracking business logic.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models import MoodEntry, User


class MoodService:
    """Service for mood tracking operations."""
    
    @staticmethod
    def track_mood(
        db: Session,
        user_id: str,
        mood: str,
        intensity: int = 3,
        note: Optional[str] = None
    ) -> MoodEntry:
        """
        Track user's mood.
        
        Args:
            db: Database session
            user_id: User ID
            mood: Mood type (happy, neutral, sad, frustrated, grateful)
            intensity: Intensity level (1-5)
            note: Optional note
            
        Returns:
            Created MoodEntry
        """
        mood_entry = MoodEntry(
            user_id=user_id,
            mood=mood.lower(),
            intensity=max(1, min(5, intensity)),  # Clamp to 1-5
            note=note,
            source='user_logged'
        )
        
        db.add(mood_entry)
        db.commit()
        db.refresh(mood_entry)
        
        return mood_entry
    
    @staticmethod
    def get_mood_history(
        db: Session,
        user_id: str,
        days: int = 7
    ) -> List[MoodEntry]:
        """
        Get user's mood history for the last N days.
        
        Args:
            db: Database session
            user_id: User ID
            days: Number of days to look back
            
        Returns:
            List of MoodEntry objects
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return db.query(MoodEntry).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= cutoff_date
        ).order_by(desc(MoodEntry.created_at)).all()
    
    @staticmethod
    def get_mood_stats(
        db: Session,
        user_id: str,
        days: int = 7
    ) -> Dict:
        """
        Get mood statistics.
        
        Args:
            db: Database session
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            Dictionary with mood statistics
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get mood distribution
        mood_distribution = db.query(
            MoodEntry.mood,
            func.count(MoodEntry.id).label('count')
        ).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= cutoff_date
        ).group_by(MoodEntry.mood).all()
        
        # Get average intensity
        avg_intensity = db.query(
            func.avg(MoodEntry.intensity)
        ).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= cutoff_date
        ).scalar() or 0
        
        # Get total check-ins
        total_checkins = db.query(func.count(MoodEntry.id)).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= cutoff_date
        ).scalar() or 0
        
        # Calculate distribution percentages
        distribution = {}
        for mood, count in mood_distribution:
            percentage = (count / total_checkins * 100) if total_checkins > 0 else 0
            distribution[mood] = {
                'count': count,
                'percentage': round(percentage, 1)
            }
        
        return {
            'total_checkins': total_checkins,
            'average_intensity': round(float(avg_intensity), 2),
            'distribution': distribution,
            'period_days': days
        }
    
    @staticmethod
    def get_mood_timeline(
        db: Session,
        user_id: str,
        days: int = 7
    ) -> List[Dict]:
        """
        Get mood timeline data for charts.
        
        Args:
            db: Database session
            user_id: User ID
            days: Number of days
            
        Returns:
            List of daily mood averages
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily averages
        daily_moods = db.query(
            func.date(MoodEntry.created_at).label('date'),
            func.avg(MoodEntry.intensity).label('avg_intensity'),
            func.count(MoodEntry.id).label('count')
        ).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= cutoff_date
        ).group_by(
            func.date(MoodEntry.created_at)
        ).order_by('date').all()
        
        timeline = []
        for date, avg_intensity, count in daily_moods:
            timeline.append({
                'date': date.isoformat(),
                'average_intensity': round(float(avg_intensity), 2),
                'check_ins': count
            })
        
        return timeline
