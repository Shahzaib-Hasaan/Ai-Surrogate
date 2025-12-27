"""
Emotion Detection Service

Extracts emotion tags from AI responses.
"""

import logging
import re
from typing import Optional, Dict, Tuple

logger = logging.getLogger(__name__)


def extract_emotion_from_response(
    user_message: str,
    ai_response: str
) -> Tuple[str, Dict[str, any]]:
    """
    Extract emotion tag from AI response.
    
    AI adds "EMOTION: [name]" at the end of response.
    We extract it and return clean response + emotion data.
    
    Args:
        user_message: Original user message
        ai_response: AI's response with EMOTION tag
        
    Returns:
        Tuple of (clean_response, emotion_data)
        - clean_response: Response without EMOTION tag
        - emotion_data: dict with emotion, confidence, intensity
    """
    
    # Look for EMOTION tag (can be on same line or new line)
    emotion_pattern = r'\s*EMOTION:\s*(\w+)\s*$'
    match = re.search(emotion_pattern, ai_response, re.IGNORECASE)
    
    if match:
        # Extract emotion
        detected_emotion = match.group(1).lower()
        
        # Remove EMOTION tag from response
        clean_response = re.sub(emotion_pattern, '', ai_response, flags=re.IGNORECASE).strip()
        
        # Estimate intensity from user message
        intensity = estimate_intensity(user_message)
        
        # High confidence since AI explicitly tagged it
        confidence = 0.9
        
        emotion_data = {
            "emotion": detected_emotion,
            "confidence": confidence,
            "intensity": intensity
        }
        
        logger.info(f"✅ Emotion extracted: {detected_emotion} (confidence: {confidence:.0%})")
        return clean_response, emotion_data
    
    else:
        # Fallback: No emotion tag found
        logger.warning("⚠️ No EMOTION tag found in AI response")
        
        intensity = estimate_intensity(user_message)
        
        emotion_data = {
            "emotion": "neutral",
            "confidence": 0.5,
            "intensity": intensity
        }
        
        return ai_response, emotion_data


def estimate_intensity(message: str) -> float:
    """
    Estimate emotional intensity from message characteristics.
    
    Args:
        message: User's message
        
    Returns:
        Intensity score (0.0 to 1.0)
    """
    intensity = 0.3  # Base intensity
    
    # Exclamation marks increase intensity
    exclamations = message.count('!')
    intensity += min(exclamations * 0.15, 0.4)
    
    # ALL CAPS increases intensity
    if message.isupper() and len(message) > 5:
        intensity += 0.2
    
    # Question marks (confusion/concern)
    questions = message.count('?')
    if questions > 1:
        intensity += 0.1
    
    # Repeated letters (e.g., "sooo", "nooo")
    if re.search(r'(.)\1{2,}', message):
        intensity += 0.15
    
    # Cap at 1.0
    return min(intensity, 1.0)


def get_emotion_emoji(emotion: str) -> str:
    """Get emoji for emotion."""
    emoji_map = {
        "happy": "😊",
        "excited": "🎉",
        "sad": "💙",
        "angry": "😤",
        "frustrated": "🌿",
        "anxious": "🫂",
        "confused": "📚",
        "grateful": "✨",
        "neutral": "😊"
    }
    return emoji_map.get(emotion, "😊")
