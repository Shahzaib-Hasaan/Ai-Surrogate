"""
AI Service for Mistral AI Integration

Handles intelligent response generation using Mistral AI API.
Compatible with mistralai>=1.0.0
"""

import os
import logging
from typing import List, Dict, Optional
from mistralai import Mistral

from app.config import settings
from app.models import Message
from sqlalchemy.orm import Session
from app.services.agent_service import get_agent

logger = logging.getLogger(__name__)

# Initialize Mistral client
mistral_client = None


def initialize_mistral_client():
    """Initialize Mistral AI client with API key."""
    global mistral_client
    try:
        api_key = settings.MISTRAL_API_KEY
        mistral_client = Mistral(api_key=api_key)
        logger.info("Mistral AI client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Mistral client: {e}")
        raise


def build_conversation_context(
    conversation_id: str,
    db: Session,
    max_messages: int = 10
) -> List[Dict]:
    """
    Build conversation context from message history.
    
    Args:
        conversation_id: ID of the conversation
        db: Database session
        max_messages: Maximum number of messages to include
        
    Returns:
        List of message dicts in Mistral format
    """
    try:
        # Get recent messages from conversation
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(max_messages)
            .all()
        )
        
        # Reverse to get chronological order
        messages = list(reversed(messages))
        
        # Convert to Mistral message format (dicts)
        context = []
        for msg in messages:
            role = "user" if msg.is_from_user else "assistant"
            context.append({"role": role, "content": msg.content})
        
        return context
    except Exception as e:
        logger.error(f"Error building context: {e}")
        return []


async def generate_ai_response(
    user_message: str,
    user_id: str,
    conversation_id: Optional[str] = None,
    db: Optional[Session] = None,
    use_memory: bool = True
) -> str:
    """
    Generate AI response using Mistral AI.
    
    Args:
        user_message: The user's message
        conversation_id: Optional conversation ID for context
        db: Optional database session for context
        
    Returns:
        AI-generated response string
    """
    global mistral_client
    
    # Initialize client if not already done
    if mistral_client is None:
        initialize_mistral_client()
    
    try:
        # Build messages array
        messages = []
        
        # Add system message for personality
        system_message = ChatMessage(
            role="system",
            content=(
                "You are a helpful, friendly AI assistant. "
                "Provide clear, concise, and helpful responses. "
                "Be conversational and engaging."
            )
        )
        messages.append(system_message)
        
        # Add conversation context if available
        if conversation_id and db:
            context = build_conversation_context(conversation_id, db)
            messages.extend(context)
        
        # Add current user message
        messages.append(ChatMessage(role="user", content=user_message))
        
        # Call Mistral API
        logger.info(f"Calling Mistral API with {len(messages)} messages")
        
        response = mistral_client.chat(
            model=settings.MISTRAL_CHAT_MODEL,
            messages=messages,
            temperature=settings.AI_TEMPERATURE,
            max_tokens=settings.MAX_RESPONSE_TOKENS,
        )
        
        # Extract response text
        ai_response = response.choices[0].message.content
        
        logger.info(f"Mistral API response received: {len(ai_response)} chars")
        
        return ai_response
        
    except Exception as e:
        logger.error(f"Mistral API error: {e}")
        # Fallback to echo
        return f"Echo: {user_message}"


async def stream_ai_response(
    user_message: str,
    user_id: str,
    conversation_id: Optional[str] = None,
    db: Optional[Session] = None
):
    """
    Stream AI response using Mistral AI with real-time chunks and memory.
    
    Yields response chunks as they arrive for typewriter effect.
    
    Args:
        user_message: The user's message
        user_id: User ID for memory retrieval
        conversation_id: Optional conversation ID for context
        db: Optional database session for context
        
    Yields:
        String chunks of the AI response
    """
    global mistral_client
    
    # Initialize client if not already done
    if mistral_client is None:
        initialize_mistral_client()
    
    try:
        # Build messages array
        messages = []
        
        # Memory is handled by Agno's built-in system (agno_memory.db)
        
        # Get agent with personality (has emotion-aware system prompt built-in)
        agent = get_agent("default")  # Can be made configurable per user
        logger.info(f"🎭 Using {agent.personality} personality")
        
        # Use Agno agent to generate response
        # Agent handles system prompt, memory, and emotion detection internally
        response_text = agent.run(user_message)
        
        # Agno agent generates response (includes EMOTION tag)
        ai_response = response_text
        
        # Simulate streaming by yielding chunks
        # Split into words for smooth streaming
        words = ai_response.split()
        for i, word in enumerate(words):
            # Yield word with space (except last word)
            if i < len(words) - 1:
                yield word + " "
            else:
                yield word
        
        logger.info(f"Streaming complete: {len(ai_response)} chars")
        
    except Exception as e:
        logger.error(f"Mistral streaming error: {e}")
        # Fallback to echo in chunks
        echo_message = f"Echo: {user_message}"
        words = echo_message.split()
        for i, word in enumerate(words):
            if i < len(words) - 1:
                yield word + " "
            else:
                yield word


async def generate_conversation_title(
    first_user_message: str,
    first_ai_response: str
) -> str:
    """
    Generate a short title for a conversation based on first exchange.
    
    Uses mistral-small-latest for cost-effective title generation.
    
    Args:
        first_user_message: The first message from user
        first_ai_response: The AI's first response
        
    Returns:
        A short title (3-6 words)
    """
    global mistral_client
    
    # Initialize client if not already done
    if mistral_client is None:
        initialize_mistral_client()
    
    try:
        # Create prompt for title generation
        prompt = f"""Based on this conversation exchange, generate a short, descriptive title (3-6 words maximum).

User: {first_user_message}
Assistant: {first_ai_response}

Title:"""
        
        messages = [ChatMessage(role="user", content=prompt)]
        
        # Call Mistral API with small model
        response = mistral_client.chat(
            model=settings.MISTRAL_TITLE_MODEL,
            messages=messages,
            temperature=0.5,  # Lower temperature for more focused titles
            max_tokens=20,  # Short titles only
        )
        
        # Extract and clean title
        title = response.choices[0].message.content.strip()
        
        # Remove quotes if present
        title = title.strip('"').strip("'")
        
        # Limit length
        if len(title) > 50:
            title = title[:47] + "..."
        
        logger.info(f"Generated title: {title}")
        
        return title
        
    except Exception as e:
        logger.error(f"Title generation error: {e}")
        # Fallback to first few words of user message
        words = first_user_message.split()[:4]
        return " ".join(words) + ("..." if len(first_user_message.split()) > 4 else "")


def count_tokens_estimate(text: str) -> int:
    """
    Estimate token count for text.
    Simple estimation: ~4 characters per token.
    
    Args:
        text: Text to count tokens for
        
    Returns:
        Estimated token count
    """
    return len(text) // 4


def optimize_context(
    messages: List[Dict],
    max_tokens: int = 4000
) -> List[Dict]:
    """
    Optimize context to fit within token limit.
    
    Args:
        messages: List of message dicts
        max_tokens: Maximum tokens allowed
        
    Returns:
        Optimized list of messages
    """
    total_tokens = sum(count_tokens_estimate(msg["content"]) for msg in messages)
    
    if total_tokens <= max_tokens:
        return messages
    
    # Keep system message and recent messages
    system_msg = messages[0] if messages and messages[0]["role"] == "system" else None
    user_messages = messages[1:] if system_msg else messages
    
    # Keep most recent messages
    optimized = []
    if system_msg:
        optimized.append(system_msg)
    
    current_tokens = count_tokens_estimate(system_msg["content"]) if system_msg else 0
    
    # Add messages from most recent backwards
    for msg in reversed(user_messages):
        msg_tokens = count_tokens_estimate(msg["content"])
        if current_tokens + msg_tokens <= max_tokens:
            optimized.insert(1 if system_msg else 0, msg)
            current_tokens += msg_tokens
        else:
            break
    
    return optimized
