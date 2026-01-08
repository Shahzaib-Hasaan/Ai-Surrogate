"""
Chat Orchestrator - Hybrid Architecture

Manual orchestration with PostgreSQL context + Agno agents for specialized tasks.
This gives us full control and debuggability while keeping agent capabilities.
"""

import logging
from typing import Optional
from sqlalchemy.orm import Session
from mistralai import Mistral

from app.config import settings
from app.models import Message
from app.services.intent_detector import get_intent_detector
from app.services.search_service import get_search_service

logger = logging.getLogger(__name__)


class ChatOrchestrator:
    """
    Hybrid AI orchestrator.
    
    - Manual control with direct Mistral API for simple chats
    - Agno agents on-demand for specialized tasks
    - Full PostgreSQL context integration
    """
    
    def __init__(self):
        """Initialize orchestrator with Mistral client."""
        self.mistral = Mistral(api_key=settings.MISTRAL_API_KEY)
        self._finance_agent = None
        self.intent_detector = get_intent_detector()
        self.search_service = get_search_service()
        logger.info("✅ Chat Orchestrator initialized")
    
    def get_conversation_history(
        self,
        conversation_id: str,
        db: Session,
        max_messages: int = 10
    ) -> list[dict]:
        """
        Get conversation history from PostgreSQL.
        
        Args:
            conversation_id: Conversation ID
            db: Database session
            max_messages: Maximum messages to retrieve
            
        Returns:
            List of message dicts in chronological order
        """
        try:
            # Get recent messages from PostgreSQL
            messages = (
                db.query(Message)
                .filter(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(max_messages)
                .all()
            )
            
            # Reverse for chronological order
            messages = list(reversed(messages))
            
            # Convert to dict format (Mistral 1.0+)
            context = []
            for msg in messages:
                role = "user" if msg.is_from_user else "assistant"
                context.append({"role": role, "content": msg.content})
            
            logger.info(f"📚 Loaded {len(context)} messages from PostgreSQL")
            return context
            
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return []
    
    async def chat(
        self,
        user_message: str,
        conversation_id: Optional[str] = None,
        db: Optional[Session] = None
    ) -> str:
        """
        Main chat method with full context and tool routing.
        
        Args:
            user_message: User's message
            conversation_id: Optional conversation ID for context
            db: Database session
            
        Returns:
            AI response string
        """
        try:
            # Detect intent
            intent = await self.intent_detector.detect_intent(user_message)
            
            # Route to appropriate tool if needed
            if intent["tool"] == "search" and intent["confidence"] > 0.7:
                return await self._handle_search_intent(user_message, conversation_id, db)
            
            # Continue with normal chat
            return await self._handle_chat(user_message, conversation_id, db)
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"I apologize, but I encountered an error. Please try again."
    
    async def _handle_search_intent(
        self,
        user_message: str,
        conversation_id: Optional[str] = None,
        db: Optional[Session] = None
    ) -> str:
        """Handle search intent by performing search and generating response."""
        try:
            # Perform search
            search_result = await self.search_service.search(user_message, num_results=5)
            
            if not search_result.get("success"):
                # Fallback to chat if search fails
                return await self._handle_chat(user_message, conversation_id, db)
            
            # Build context with search results
            search_summary = search_result.get("summary", "")
            search_results = search_result.get("results", [])
            
            # Create enhanced prompt with search results
            enhanced_message = f"""User asked: {user_message}

I found the following information:

{search_summary}

Please provide a helpful response based on this information. If the information is relevant, use it. If not, provide a general helpful response."""
            
            # Get AI response with search context
            return await self._handle_chat(enhanced_message, conversation_id, db)
            
        except Exception as e:
            logger.error(f"Search intent handling error: {e}")
            return await self._handle_chat(user_message, conversation_id, db)
    
    async def _handle_chat(
        self,
        user_message: str,
        conversation_id: Optional[str] = None,
        db: Optional[Session] = None
    ) -> str:
        """Handle normal chat without tools."""
        try:
            # Build messages array
            messages = []
            
            # System prompt with strict bilingual + emotion detection + formatting
            system_prompt = """You are a helpful, empathetic AI assistant with bilingual capabilities.

CRITICAL LANGUAGE DETECTION RULES:
Read the user's CURRENT message ONLY to determine language. Do NOT switch languages based on conversation history.

1. If the CURRENT message is in English (uses English words, Latin script) → ALWAYS respond in English
   Examples: "Hi", "How are you", "Leave me what about you", "Feeling good"
   
2. If the CURRENT message is in proper Urdu script (اردو characters) → Respond in proper Urdu (اردو)
   Examples: "کیسے ہو", "شکریہ", "آپ کیسے ہیں"
   
3. If the CURRENT message is in Roman Urdu (Urdu words but Latin script) → Respond in proper Urdu (اردو)
   Examples: "Kaise ho", "Shukriya", "Aap kaise hain"
   
4. If the CURRENT message is in Hindi → Treat as Urdu, respond in proper Urdu (اردو)

5. If the CURRENT message is in Punjabi (ਪੰਜਾਬੀ) → Respond in Punjabi (ਪੰਜਾਬੀ)
   Examples: "ਕਿਵੇਂ ਹੋ", "ਧੰਨਵਾਦ", "ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ"

6. If the CURRENT message requests another language → Politely decline in BOTH languages:
   "I only speak English, Urdu, and Punjabi. میں صرف انگریزی، اردو اور پنجابی بولتا ہوں۔"

IMPORTANT:
- Do NOT mix languages in your response
- Do NOT switch languages unless user's CURRENT message is clearly in that language
- English messages MUST get English responses
- Be consistent with your language choice throughout the response
- Support English, Urdu (اردو), and Punjabi (ਪੰਜਾਬੀ)

FORMATTING RULES (CRITICAL):
- Use proper line breaks and paragraphs for readability
- Break long responses into multiple paragraphs
- Use markdown formatting:
  * **Bold** for emphasis
  * *Italic* for subtle emphasis
  * Numbered lists (1. 2. 3.) for steps or ordered items
  * Bullet points (- item) for unordered lists
- Add blank lines between paragraphs
- Keep paragraphs short (2-4 sentences max)
- Use line breaks after greetings or before conclusions

GOOD FORMATTING EXAMPLE:
"Great energy! 😊 Here are some fun ideas we can do together:

1. **Play a quick game** – Like 20 Questions, Would You Rather, or trivia!
2. **Tell jokes** – I've got some silly ones ready if you want a laugh.
3. **Learn something new** – A fun fact, a word in another language, or even a random skill.

What sounds fun to you? 🎉"

BAD FORMATTING EXAMPLE (DO NOT DO THIS):
"Great energy! 😊 Here are some fun ideas we can do together: 1. **Play a quick game** – Like 20 Questions, Would You Rather, or trivia! 2. **Tell jokes** – I've got some silly ones ready if you want a laugh. 3. **Learn something new** – A fun fact, a word in another language, or even a random skill. What sounds fun to you? 🎉"

RESPONSE QUALITY:
- Be helpful, friendly, conversational
- Use markdown formatting for better readability
- When responding in Urdu, use ONLY proper Urdu script (اردو), never Roman Urdu
- Structure your responses with clear paragraphs and spacing

EMOTION DETECTION:
At the END of EVERY response, add a new line with:
EMOTION: [emotion]

Where [emotion] is ONE of: happy, sad, angry, anxious, neutral, excited, confused, frustrated, grateful

Example (English):
"I'm here to help! How can I assist you today?

EMOTION: neutral"

Example (Urdu):
"میں آپ کی مدد کے لیے حاضر ہوں! آج میں آپ کی کیسے مدد کر سکتا ہوں؟

EMOTION: neutral"
"""
            
            messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history from PostgreSQL
            if conversation_id and db:
                history = self.get_conversation_history(conversation_id, db)
                messages.extend(history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            logger.info(f"🤖 Calling Mistral with {len(messages)} messages (system + {len(messages)-2} history + current)")
            
            # Direct Mistral API call (version 1.0+)
            response = self.mistral.chat.complete(
                model="mistral-large-latest",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            logger.info(f"✅ Response generated: {len(ai_response)} chars")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"I apologize, but I encountered an error. Please try again."
    
    async def stream_chat(
        self,
        user_message: str,
        conversation_id: Optional[str] = None,
        db: Optional[Session] = None
    ):
        """
        Stream chat response word by word.
        
        Args:
            user_message: User's message
            conversation_id: Optional conversation ID for context
            db: Database session
            
        Yields:
            String chunks
        """
        try:
            # Get complete response
            response = await self.chat(user_message, conversation_id, db)
            
            # Stream word by word
            words = response.split()
            for i, word in enumerate(words):
                if i < len(words) - 1:
                    yield word + " "
                else:
                    yield word
                    
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"Echo: {user_message}"


# Global orchestrator instance
_orchestrator = None


def get_orchestrator() -> ChatOrchestrator:
    """Get or create global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ChatOrchestrator()
    return _orchestrator
