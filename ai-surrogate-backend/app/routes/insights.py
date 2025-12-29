"""
Insights Routes

API endpoints for user insights and analytics.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.routes.auth import get_current_user
from app.services.insights_service import InsightsService


router = APIRouter(prefix="/api/insights", tags=["insights"])


@router.get("/summary")
async def get_insights_summary(
    period: str = Query('week', regex='^(week|month|all)$'),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive insights summary.
    
    **Query Parameters:**
    - period: 'week', 'month', or 'all' (default: 'week')
    
    **Returns:**
    - wellness_score: Overall wellness score (0-100)
    - emotion_timeline: Daily emotion scores
    - emotion_distribution: Emotion breakdown with percentages
    - conversation_stats: Message and conversation statistics
    - mood_stats: Mood check-in statistics
    """
    summary = InsightsService.get_summary(
        db=db,
        user_id=str(current_user.id),
        period=period
    )
    
    return summary


@router.get("/ai-analysis")
async def get_ai_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered analysis of emotional patterns.
    
    **Returns:**
    - insights: Key insights about emotional patterns
    - patterns: Detected patterns
    - recommendations: Personalized recommendations
    
    Note: This is a placeholder. Full AI analysis will be implemented in Phase 2.
    """
    # TODO: Implement AI analysis using LLM
    # For now, return placeholder data
    
    summary = InsightsService.get_summary(
        db=db,
        user_id=str(current_user.id),
        period='week'
    )
    
    wellness_score = summary['wellness_score']
    
    # Generate simple insights based on data
    insights = []
    patterns = []
    recommendations = []
    
    if wellness_score >= 80:
        insights.append("You're maintaining excellent emotional well-being!")
        recommendations.append("Keep up your current self-care routine")
    elif wellness_score >= 60:
        insights.append("Your emotional health is good overall")
        recommendations.append("Consider daily mood check-ins for better tracking")
    else:
        insights.append("Your wellness score suggests room for improvement")
        recommendations.append("Try to check in with your emotions more regularly")
    
    # Check mood distribution
    if summary.get('emotion_distribution'):
        top_emotion = summary['emotion_distribution'][0]
        insights.append(f"Your most common emotion this week was {top_emotion['emotion']}")
    
    # Check conversation engagement
    conv_stats = summary.get('conversation_stats', {})
    if conv_stats.get('total_conversations', 0) > 5:
        patterns.append("High engagement with AI conversations")
    
    return {
        'insights': insights,
        'patterns': patterns,
        'recommendations': recommendations,
        'wellness_score': wellness_score,
        'period': 'week'
    }
