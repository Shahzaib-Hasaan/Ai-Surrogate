

@router.delete(
    "/conversations/{conversation_id}",
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
    
    Verifies ownership before deletion. Cascade delete removes all messages.
    
    Args:
        conversation_id: UUID of the conversation to delete
        
    Returns:
        Success message
        
    Raises:
        404: Conversation not found or not owned by user
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
    
    # Delete conversation (cascade will delete messages and emotion history)
    db.delete(conversation)
    db.commit()
    
    return {
        "message": "Conversation deleted successfully",
        "conversation_id": str(conversation_id)
    }
