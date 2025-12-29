"""
Conversation Naming Service

Automatically generates meaningful conversation titles using Mistral AI.
"""

import asyncio
from typing import Optional
from sqlalchemy.orm import Session
from mistralai import Mistral

from app.config import settings
from app.models import Conversation


async def generate_conversation_title(
    user_message: str,
    ai_response: Optional[str] = None
) -> str:
    """
    Generate a concise conversation title using Mistral AI.
    
    Args:
        user_message: The first user message in the conversation
        ai_response: Optional AI response for additional context
        
    Returns:
        Generated title (max 50 characters)
    """
    try:
        client = Mistral(api_key=settings.MISTRAL_API_KEY)
        
        # Create prompt for title generation
        context = f"User: {user_message}"
        if ai_response:
            context += f"\nAssistant: {ai_response}"
        
        prompt = f"""Based on this conversation start, generate a short, descriptive title (max 5 words, 50 characters).
The title should capture the main topic or intent.

Conversation:
{context}

Generate ONLY the title, nothing else. Be concise and specific."""

        # Use Mistral small model for efficiency
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more focused titles
            max_tokens=20
        )
        
        # Extract title
        title = response.choices[0].message.content.strip()
        
        # Remove quotes if present
        title = title.strip('"\'')
        
        # Truncate if too long
        if len(title) > 50:
            title = title[:47] + "..."
        
        return title
        
    except Exception as e:
        print(f"⚠️ Title generation failed: {e}")
        # Fallback: Use first few words of user message
        words = user_message.split()[:5]
        fallback_title = " ".join(words)
        if len(fallback_title) > 50:
            fallback_title = fallback_title[:47] + "..."
        return fallback_title


async def update_conversation_title_async(
    conversation_id: str,
    user_message: str,
    ai_response: Optional[str],
    db: Session
):
    """
    Update conversation title asynchronously (runs in background).
    
    Args:
        conversation_id: Conversation ID to update
        user_message: First user message
        ai_response: Optional AI response
        db: Database session
    """
    try:
        print(f"🏷️ Generating title for conversation {conversation_id}...")
        
        # Generate title
        title = await generate_conversation_title(user_message, ai_response)
        
        # Update conversation in database
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if conversation:
            conversation.title = title
            db.commit()
            print(f"✅ Conversation titled: '{title}'")
        else:
            print(f"⚠️ Conversation {conversation_id} not found")
            
    except Exception as e:
        print(f"❌ Failed to update conversation title: {e}")
        # Don't raise - this is a background task


def trigger_conversation_naming(
    conversation_id: str,
    user_message: str,
    ai_response: Optional[str],
    db: Session
):
    """
    Trigger conversation naming in the background (non-blocking).
    
    This function starts the naming process without waiting for it to complete.
    
    Args:
        conversation_id: Conversation ID to update
        user_message: First user message
        ai_response: Optional AI response
        db: Database session
    """
    # Create background task
    asyncio.create_task(
        update_conversation_title_async(
            conversation_id=conversation_id,
            user_message=user_message,
            ai_response=ai_response,
            db=db
        )
    )
    print(f"🚀 Background task started for conversation naming: {conversation_id}")
