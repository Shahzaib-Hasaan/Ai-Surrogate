"""
Conversation Management API routes.

Endpoints:
- DELETE /api/conversations/{conversation_id} - Delete a conversation
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Conversation, Message as DBMessage
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a conversation",
    description="Delete a conversation and all its messages"
)
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a conversation and all associated messages.
    
    Verifies ownership before deletion. Manually deletes related records
    to handle foreign key constraints properly.
    """
    # Verify conversation exists and belongs to user
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    try:
        # First, delete emotion_history records for this conversation
        try:
            from app.models import EmotionHistory
            db.query(EmotionHistory).filter(
                EmotionHistory.conversation_id == str(conversation_id)
            ).delete()
        except Exception:
            pass  # EmotionHistory might not exist
        
        # Then, delete all messages in the conversation
        db.query(DBMessage).filter(
            DBMessage.conversation_id == str(conversation_id)
        ).delete()
        
        # Finally, delete the conversation itself
        db.delete(conversation)
        db.commit()
        
        return {
            "message": "Conversation deleted successfully",
            "conversation_id": str(conversation_id)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}"
        )
