"""Add emotion_history table

Revision ID: add_emotion_history
Revises: 
Create Date: 2024-12-27

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_emotion_history'
down_revision = None  # Update this to your latest migration
branch_labels = None
depends_on = None


def upgrade():
    # Create emotion_history table
    op.create_table(
        'emotion_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('conversations.id'), nullable=False),
        sa.Column('message_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('messages.id'), nullable=False),
        sa.Column('emotion', sa.String(50), nullable=False),
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.8'),
        sa.Column('intensity', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('user_message', sa.String, nullable=False),
        sa.Column('ai_response', sa.String, nullable=False),
        sa.Column('detected_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    )
    
    # Create indexes for better query performance
    op.create_index('ix_emotion_history_user_id', 'emotion_history', ['user_id'])
    op.create_index('ix_emotion_history_conversation_id', 'emotion_history', ['conversation_id'])
    op.create_index('ix_emotion_history_emotion', 'emotion_history', ['emotion'])
    op.create_index('ix_emotion_history_detected_at', 'emotion_history', ['detected_at'])


def downgrade():
    # Drop indexes
    op.drop_index('ix_emotion_history_detected_at', 'emotion_history')
    op.drop_index('ix_emotion_history_emotion', 'emotion_history')
    op.drop_index('ix_emotion_history_conversation_id', 'emotion_history')
    op.drop_index('ix_emotion_history_user_id', 'emotion_history')
    
    # Drop table
    op.drop_table('emotion_history')
