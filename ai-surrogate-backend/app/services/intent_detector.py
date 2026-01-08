"""
Intent Detector - Detects user intent for tool routing

Determines if user wants to:
- Search the web
- Create calendar events
- Create documents
- General chat
"""

import logging
from typing import Dict, Any, Optional
from mistralai import Mistral

from app.config import settings

logger = logging.getLogger(__name__)


class IntentDetector:
    """
    Detects user intent to route to appropriate tools or agents.
    """
    
    def __init__(self):
        """Initialize intent detector."""
        self.mistral = Mistral(api_key=settings.MISTRAL_API_KEY)
    
    async def detect_intent(self, user_message: str) -> Dict[str, Any]:
        """
        Detect user intent from message.
        
        Args:
            user_message: User's message
            
        Returns:
            Dict with intent type and confidence
        """
        try:
            # Simple keyword-based detection first (fast)
            intent = self._detect_keywords(user_message)
            if intent["confidence"] > 0.7:
                return intent
            
            # Use LLM for more complex detection
            return await self._detect_with_llm(user_message)
            
        except Exception as e:
            logger.error(f"Intent detection error: {e}")
            return {
                "intent": "chat",
                "confidence": 0.5,
                "tool": None
            }
    
    def _detect_keywords(self, message: str) -> Dict[str, Any]:
        """
        Fast keyword-based intent detection.
        
        Returns:
            Dict with intent, confidence, and tool
        """
        message_lower = message.lower()
        
        # Search intent
        search_keywords = [
            "search", "find", "look up", "google", "what is", "who is",
            "when did", "where is", "how to", "latest", "news about",
            "information about", "tell me about"
        ]
        
        if any(keyword in message_lower for keyword in search_keywords):
            return {
                "intent": "search",
                "confidence": 0.8,
                "tool": "search"
            }
        
        # Calendar intent
        calendar_keywords = [
            "schedule", "meeting", "appointment", "event", "calendar",
            "remind me", "set a reminder", "book", "reserve"
        ]
        
        if any(keyword in message_lower for keyword in calendar_keywords):
            return {
                "intent": "calendar",
                "confidence": 0.75,
                "tool": "calendar"
            }
        
        # Document intent
        doc_keywords = [
            "create document", "write document", "draft", "generate document",
            "make a document", "create a file"
        ]
        
        if any(keyword in message_lower for keyword in doc_keywords):
            return {
                "intent": "document",
                "confidence": 0.75,
                "tool": "docs"
            }
        
        # Default to chat
        return {
            "intent": "chat",
            "confidence": 0.6,
            "tool": None
        }
    
    async def _detect_with_llm(self, message: str) -> Dict[str, Any]:
        """
        Use LLM for more sophisticated intent detection.
        
        Returns:
            Dict with intent, confidence, and tool
        """
        try:
            prompt = f"""Analyze this user message and determine their intent. Respond with ONLY one word: "search", "calendar", "document", or "chat".

User message: "{message}"

Intent:"""
            
            response = self.mistral.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=10
            )
            
            intent_text = response.choices[0].message.content.strip().lower()
            
            # Map to intent
            intent_map = {
                "search": {"intent": "search", "tool": "search", "confidence": 0.85},
                "calendar": {"intent": "calendar", "tool": "calendar", "confidence": 0.85},
                "document": {"intent": "document", "tool": "docs", "confidence": 0.85},
                "chat": {"intent": "chat", "tool": None, "confidence": 0.85}
            }
            
            result = intent_map.get(intent_text, intent_map["chat"])
            logger.info(f"🎯 Detected intent: {result['intent']} (confidence: {result['confidence']})")
            
            return result
            
        except Exception as e:
            logger.error(f"LLM intent detection error: {e}")
            return {
                "intent": "chat",
                "confidence": 0.5,
                "tool": None
            }


# Global intent detector instance
_intent_detector = None


def get_intent_detector() -> IntentDetector:
    """Get or create global intent detector instance."""
    global _intent_detector
    if _intent_detector is None:
        _intent_detector = IntentDetector()
    return _intent_detector
