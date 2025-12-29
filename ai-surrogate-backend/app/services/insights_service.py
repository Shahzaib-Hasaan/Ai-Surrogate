"""
Insights Service

Provides analytics and insights from mood and emotion data.
"""

from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models import MoodEntry, EmotionHistory, Message, User
from app.services.mood_service import MoodService


class InsightsService:
    """Service for generating user insights and analytics."""
    
    @staticmethod
    def get_summary(
        db: Session,
        user_id: str,
        period: str = 'week'
    ) -> Dict:
        """
        Get comprehensive insights summary.
        
        Args:
            db: Database session
            user_id: User ID
            period: 'week', 'month', or 'all'
            
        Returns:
            Dictionary with all insights data
        """
        days = InsightsService._get_days_from_period(period)
        
        return {
            'wellness_score': InsightsService.calculate_wellness_score(db, user_id, days),
            'emotion_timeline': InsightsService.get_emotion_timeline(db, user_id, days),
            'emotion_distribution': InsightsService.get_emotion_distribution(db, user_id, days),
            'conversation_stats': InsightsService.get_conversation_stats(db, user_id, days),
            'mood_stats': MoodService.get_mood_stats(db, user_id, days),
            'period': period,
            'period_days': days
        }
    
    @staticmethod
    def calculate_wellness_score(
        db: Session,
        user_id: str,
        days: int = 7
    ) -> int:
        """
        Calculate wellness score (0-100).
        
        Based on:
        - Mood check-in frequency
        - Average mood intensity
        - Emotion positivity
        - Conversation engagement
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get mood data
        mood_entries = db.query(MoodEntry).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= cutoff_date
        ).all()
        
        # Get emotion data
        emotions = db.query(EmotionHistory).filter(
            EmotionHistory.user_id == user_id,
            EmotionHistory.detected_at >= cutoff_date
        ).all()
        
        score = 50  # Base score
        
        # Factor 1: Mood check-in frequency (0-20 points)
        checkin_frequency = len(mood_entries) / days
        score += min(checkin_frequency * 10, 20)
        
        # Factor 2: Average mood intensity (0-30 points)
        if mood_entries:
            positive_moods = ['happy', 'grateful']
            positive_count = sum(1 for m in mood_entries if m.mood in positive_moods)
            positive_ratio = positive_count / len(mood_entries)
            score += positive_ratio * 30
        
        # Factor 3: Emotion positivity (0-20 points)
        if emotions:
            positive_emotions = ['happy', 'excited', 'grateful']
            positive_count = sum(1 for e in emotions if e.emotion in positive_emotions)
            positive_ratio = positive_count / len(emotions)
            score += positive_ratio * 20
        
        # Factor 4: Engagement (0-10 points)
        message_count = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.created_at >= cutoff_date
        ).scalar() or 0
        
        if message_count > 0:
            score += min(message_count / 10, 10)
        
        return min(int(score), 100)
    
    @staticmethod
    def get_emotion_timeline(
        db: Session,
        user_id: str,
        days: int = 7
    ) -> List[Dict]:
        """
        Get emotion timeline combining mood entries and detected emotions.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Map emotions to scores (1-5)
        emotion_scores = {
            'happy': 5, 'excited': 5, 'grateful': 5,
            'neutral': 3,
            'sad': 2, 'anxious': 2, 'confused': 2,
            'angry': 1, 'frustrated': 1
        }
        
        # Get daily averages from mood entries
        mood_timeline = MoodService.get_mood_timeline(db, user_id, days)
        
        # Get daily averages from detected emotions
        emotion_daily = db.query(
            func.date(EmotionHistory.detected_at).label('date'),
            func.avg(EmotionHistory.intensity).label('avg_intensity'),
            func.count(EmotionHistory.id).label('count')
        ).filter(
            EmotionHistory.user_id == user_id,
            EmotionHistory.detected_at >= cutoff_date
        ).group_by(
            func.date(EmotionHistory.detected_at)
        ).all()
        
        # Combine both sources
        timeline_dict = {}
        
        for entry in mood_timeline:
            timeline_dict[entry['date']] = {
                'date': entry['date'],
                'user_mood': entry['average_intensity'],
                'detected_emotion': None,
                'combined_score': entry['average_intensity']
            }
        
        for date, avg_intensity, count in emotion_daily:
            date_str = date.isoformat()
            if date_str in timeline_dict:
                timeline_dict[date_str]['detected_emotion'] = avg_intensity * 5
                # Average both sources
                timeline_dict[date_str]['combined_score'] = (
                    timeline_dict[date_str]['user_mood'] + avg_intensity * 5
                ) / 2
            else:
                timeline_dict[date_str] = {
                    'date': date_str,
                    'user_mood': None,
                    'detected_emotion': avg_intensity * 5,
                    'combined_score': avg_intensity * 5
                }
        
        return sorted(timeline_dict.values(), key=lambda x: x['date'])
    
    @staticmethod
    def get_emotion_distribution(
        db: Session,
        user_id: str,
        days: int = 7
    ) -> List[Dict]:
        """
        Get emotion distribution for pie chart.
        Combines mood entries and detected emotions.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get mood distribution
        mood_dist = db.query(
            MoodEntry.mood,
            func.count(MoodEntry.id).label('count')
        ).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= cutoff_date
        ).group_by(MoodEntry.mood).all()
        
        # Get emotion distribution
        emotion_dist = db.query(
            EmotionHistory.emotion,
            func.count(EmotionHistory.id).label('count')
        ).filter(
            EmotionHistory.user_id == user_id,
            EmotionHistory.detected_at >= cutoff_date
        ).group_by(EmotionHistory.emotion).all()
        
        # Combine and calculate percentages
        combined = {}
        total = 0
        
        for mood, count in mood_dist:
            combined[mood] = combined.get(mood, 0) + count
            total += count
        
        for emotion, count in emotion_dist:
            combined[emotion] = combined.get(emotion, 0) + count
            total += count
        
        # Convert to list with percentages
        distribution = []
        for emotion, count in combined.items():
            percentage = (count / total * 100) if total > 0 else 0
            distribution.append({
                'emotion': emotion,
                'count': count,
                'percentage': round(percentage, 1)
            })
        
        return sorted(distribution, key=lambda x: x['count'], reverse=True)
    
    @staticmethod
    def get_conversation_stats(
        db: Session,
        user_id: str,
        days: int = 7
    ) -> Dict:
        """
        Get conversation statistics.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Total messages
        total_messages = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.created_at >= cutoff_date
        ).scalar() or 0
        
        # User messages only
        user_messages = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.is_from_user == True,
            Message.created_at >= cutoff_date
        ).scalar() or 0
        
        # Total conversations (unique conversation IDs)
        total_conversations = db.query(
            func.count(func.distinct(Message.conversation_id))
        ).filter(
            Message.user_id == user_id,
            Message.created_at >= cutoff_date
        ).scalar() or 0
        
        # Mood check-ins
        mood_checkins = db.query(func.count(MoodEntry.id)).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= cutoff_date
        ).scalar() or 0
        
        return {
            'total_messages': total_messages,
            'user_messages': user_messages,
            'total_conversations': total_conversations,
            'mood_checkins': mood_checkins
        }
    
    @staticmethod
    def _get_days_from_period(period: str) -> int:
        """Convert period string to number of days."""
        if period == 'week':
            return 7
        elif period == 'month':
            return 30
        elif period == 'all':
            return 365  # Cap at 1 year
        else:
            return 7  # Default to week
