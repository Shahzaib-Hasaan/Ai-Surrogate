"""
Chat API routes.

Endpoints:
- POST /api/chat/message - Send a message and get AI response
- GET /api/chat/conversations - Get all user conversations
- GET /api/chat/conversations/{conversation_id}/messages - Get messages in a conversation
"""

from typing import List
from uuid import UUID
import json
import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Conversation, Message as DBMessage
from app.schemas import MessageCreate, MessageResponse, ConversationResponse
from app.services.auth_service import get_current_user
from app.services.chat_service import (
    create_message,
    get_user_conversations,
    get_conversation_messages,
    generate_ai_response_with_context
)
from app.services.ai_service import stream_ai_response
from app.services.chat_service import create_conversation
from app.services.emotion_service import extract_emotion_from_response
from app.services.conversation_naming_service import trigger_conversation_naming

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post(
    "/message",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send a message",
    description="Send a message and get an AI response using Mistral AI"
)
async def send_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message and receive an AI response.
    
    - **content**: Message content (1-5000 characters)
    - **conversation_id**: Optional conversation ID (creates new if not provided)
    
    Uses Mistral AI for intelligent responses with conversation context.
    Falls back to echo if AI fails.
    
    Requires authentication.
    """
    try:
        # Save user message
        user_message = create_message(
            db=db,
            user=current_user,
            content=message_data.content,
            is_from_user=True,
            conversation_id=message_data.conversation_id
        )
        
        # Generate AI response with context
        ai_response_text = await generate_ai_response_with_context(
            user_message=message_data.content,
            conversation_id=str(user_message.conversation_id),
            db=db
        )
        
        # Save AI response
        ai_message = create_message(
            db=db,
            user=current_user,
            content=ai_response_text,
            is_from_user=False,
            conversation_id=user_message.conversation_id
        )
        
        return ai_message
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


@router.get(
    "/conversations",
    response_model=List[ConversationResponse],
    summary="Get all conversations",
    description="Get all conversations for the current user"
)
def get_conversations(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all conversations for the authenticated user.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (max 100)
    
    Returns conversations ordered by most recently updated.
    
    Requires authentication.
    """
    if limit > 100:
        limit = 100
    
    conversations = get_user_conversations(
        db=db,
        user=current_user,
        skip=skip,
        limit=limit
    )
    
    return conversations


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=List[MessageResponse],
    summary="Get conversation messages",
    description="Get all messages in a specific conversation"
)
def get_messages(
    conversation_id: UUID,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all messages in a conversation.
    
    - **conversation_id**: UUID of the conversation
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (max 200)
    
    Returns messages ordered chronologically (oldest first).
    
    Requires authentication and conversation ownership.
    """
    if limit > 200:
        limit = 200
    
    try:
        messages = get_conversation_messages(
            db=db,
            conversation_id=conversation_id,
            user=current_user,
            skip=skip,
            limit=limit
        )
        
        return messages
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/stream",
    summary="Stream AI response",
    description="Stream AI response in real-time using Server-Sent Events"
)
async def stream_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Stream AI response in real-time for typewriter effect.
    
    Returns Server-Sent Events (SSE) stream with response chunks.
    """
    
    async def generate_stream():
        try:
            print(f"🎬 STREAM STARTED for user: {current_user.username}")
            print(f"📝 Message content: {message_data.content}")
            
            # Create or get conversation
            conversation_id = message_data.conversation_id
            
            if not conversation_id:
                # Create new conversation
                print("📁 Creating new conversation...")
                conversation = create_conversation(
                    db=db,
                    user=current_user,
                    title="New Conversation"
                )
                conversation_id = str(conversation.id)
                print(f"✅ Created conversation: {conversation_id}")
            else:
                # Ensure conversation_id is a string
                conversation_id = str(conversation_id)
                print(f"📂 Using existing conversation: {conversation_id}")
            
            # Save user message
            print("💾 Saving user message...")
            user_msg = DBMessage(
                content=message_data.content,
                conversation_id=conversation_id,
                user_id=current_user.id,
                is_from_user=True
            )
            db.add(user_msg)
            db.commit()
            db.refresh(user_msg)
            print(f"✅ User message saved: {user_msg.id}")
            
            # Send conversation ID first
            conv_data = json.dumps({'type': 'conversation_id', 'conversation_id': conversation_id})
            yield f"data: {conv_data}\n\n"
            print(f"📤 Sent conversation_id: {conversation_id}")
            
            # Stream AI response with memory
            print("🤖 Starting AI streaming...")
            full_response = ""
            chunk_count = 0
            
            # Send initial "thinking" message to frontend immediately
            # This prevents the frontend from thinking the connection is dead
            thinking_data = json.dumps({'type': 'chunk', 'content': 'Thinking... '})
            yield f"data: {thinking_data}\n\n"
            print("📤 Sent 'Thinking...' indicator")
            
            # Stream response chunks as they arrive
            try:
                print("🔄 Starting to stream response chunks...")
                buffer = ""  # Buffer for collecting full response
                
                async for chunk in stream_ai_response(
                    user_message=message_data.content,
                    user_id=str(current_user.id),
                    conversation_id=conversation_id,
                    db=db
                ):
                    buffer += chunk
                    full_response += chunk
                    
                    # Send chunks immediately as they arrive (skip "Thinking" from orchestrator)
                    if chunk.strip() and chunk.strip() != "Thinking":
                        chunk_data = json.dumps({'type': 'chunk', 'content': chunk})
                        yield f"data: {chunk_data}\n\n"
                        chunk_count += 1
                        if chunk_count <= 5 or chunk_count % 10 == 0:  # Log first 5 and every 10th chunk
                            print(f"📦 Sent chunk {chunk_count}: '{chunk[:50]}...'")
                
                print(f"✅ AI response streamed: {len(full_response)} chars, {chunk_count} chunks")
                
            except Exception as stream_error:
                print(f"❌ Stream error during collection: {stream_error}")
                import traceback
                traceback.print_exc()
                # Send error to frontend
                error_data = json.dumps({'type': 'error', 'message': str(stream_error)})
                yield f"data: {error_data}\n\n"
                return
            
            # Extract emotion and get clean response (without EMOTION tag)
            clean_response, emotion_data = extract_emotion_from_response(
                user_message=message_data.content,
                ai_response=full_response
            )
            
            print(f"✅ Clean response: {len(clean_response)} chars")
            
            # Save AI response (clean version without EMOTION tag)
            print("💾 Saving AI message...")
            ai_msg = DBMessage(
                content=clean_response,
                conversation_id=conversation_id,
                user_id=current_user.id,
                is_from_user=False
            )
            db.add(ai_msg)
            db.commit()
            db.refresh(ai_msg)
            print(f"✅ AI message saved: {ai_msg.id}")
            
            # Save emotion to database
            try:
                from app.models import EmotionHistory
                
                emotion_record = EmotionHistory(
                    user_id=current_user.id,
                    conversation_id=conversation_id,
                    message_id=ai_msg.id,
                    emotion=emotion_data["emotion"],
                    confidence=emotion_data["confidence"],
                    intensity=emotion_data["intensity"],
                    user_message=message_data.content,
                    ai_response=clean_response
                )
                db.add(emotion_record)
                db.commit()
                print(f"🧠 Emotion detected: {emotion_data['emotion']} ({emotion_data['confidence']:.0%} confidence)")
            except Exception as emotion_error:
                print(f"⚠️ Emotion tracking failed: {emotion_error}")
            
            # Auto-generate conversation title if this is the first message
            try:
                # Count messages in this conversation (excluding current ones)
                message_count = db.query(DBMessage).filter(
                    DBMessage.conversation_id == conversation_id,
                    DBMessage.is_from_user == True
                ).count()
                
                # If this is the first user message, generate title
                if message_count == 1:
                    print(f"🏷️ First message detected, triggering conversation naming...")
                    trigger_conversation_naming(
                        conversation_id=conversation_id,
                        user_message=message_data.content,
                        ai_response=clean_response,
                        db=db
                    )
            except Exception as naming_error:
                print(f"⚠️ Conversation naming failed: {naming_error}")
            
            # Send completion
            complete_data = json.dumps({'type': 'complete', 'message_id': str(ai_msg.id)})
            yield f"data: {complete_data}\n\n"
            print("🎉 Stream complete!")
            
        except Exception as e:
            print(f"❌ STREAM ERROR: {e}")
            import traceback
            traceback.print_exc()
            # Send error
            error_data = json.dumps({'type': 'error', 'message': str(e)})
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )