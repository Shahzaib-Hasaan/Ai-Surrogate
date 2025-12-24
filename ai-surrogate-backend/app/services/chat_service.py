"""
Chat service for handling message and conversation operations.
"""

from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.models import User, Conversation, Message


def create_conversation(
    db: Session,
    user: User,
    title: Optional[str] = None
) -> Conversation:
    """
    Create a new conversation for a user.
    
    Args:
        db: Database session
        user: User who owns the conversation
        title: Optional conversation title
        
    Returns:
        Created Conversation instance
    """
    conversation = Conversation(
        user_id=user.id,
        title=title or f"Conversation {uuid4().hex[:8]}"
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation


def get_user_conversations(
    db: Session,
    user: User,
    skip: int = 0,
    limit: int = 50
) -> List[Conversation]:
    """
    Get all conversations for a user.
    
    Args:
        db: Database session
        user: User to get conversations for
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of Conversation instances
    """
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_conversation_messages(
    db: Session,
    conversation_id: UUID,
    user: User,
    skip: int = 0,
    limit: int = 100
) -> List[Message]:
    """
    Get all messages in a conversation.
    
    Args:
        db: Database session
        conversation_id: Conversation ID
        user: User requesting the messages (for authorization)
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of Message instances
        
    Raises:
        ValueError: If conversation doesn't belong to user
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id
    ).first()
    
    if not conversation:
        raise ValueError("Conversation not found or access denied")
    
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_message(
    db: Session,
    user: User,
    content: str,
    is_from_user: bool,
    conversation_id: Optional[UUID] = None
) -> Message:
    """
    Create a new message in a conversation.
    
    Args:
        db: Database session
        user: User who owns the message
        content: Message content
        is_from_user: True if message is from user, False if from AI
        conversation_id: Optional conversation ID (creates new if None)
        
    Returns:
        Created Message instance
    """
    # Create conversation if not provided
    if conversation_id is None:
        conversation = create_conversation(db, user)
        conversation_id = conversation.id
    else:
        # Verify conversation belongs to user
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id
        ).first()
        
        if not conversation:
            raise ValueError("Conversation not found or access denied")
    
    # Create message
    message = Message(
        user_id=user.id,
        conversation_id=conversation_id,
        content=content,
        is_from_user=is_from_user
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message


async def generate_ai_response_with_context(
    user_message: str,
    conversation_id: str,
    db: Session
) -> str:
    """
    Generate AI response with conversation context.
    
    Uses Mistral AI for intelligent responses.
    Falls back to echo if AI fails.
    
    Args:
        user_message: The user's message
        conversation_id: Conversation ID for context
        db: Database session
        
    Returns:
        AI-generated response string
    """
    try:
        from app.services import ai_service
        
        # Generate AI response with context
        response = await ai_service.generate_ai_response(
            user_message=user_message,
            conversation_id=conversation_id,
            db=db
        )
        
        return response
        
    except Exception as e:
        # Log error and fallback to echo
        print(f"AI generation failed: {e}")
        return f"Echo: {user_message}"
