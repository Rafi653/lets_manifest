"""Add notifications and notification_settings tables

Revision ID: a1b2c3d4e5f6
Revises: 7b202b81edfb
Create Date: 2025-11-15 04:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '7b202b81edfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add reminder fields to goals table
    op.add_column('goals', sa.Column('reminder_enabled', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('reminder_time', sa.String(length=5), nullable=True))
    op.add_column('goals', sa.Column('reminder_days_before', sa.Integer(), nullable=True))

    # Set default values for existing records
    op.execute("UPDATE goals SET reminder_enabled = FALSE WHERE reminder_enabled IS NULL")
    
    # Make reminder_enabled not nullable after setting defaults
    op.alter_column('goals', 'reminder_enabled', nullable=False)

    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('goal_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('notification_type', sa.String(length=50), nullable=False),
        sa.Column('scheduled_time', sa.DateTime(), nullable=False),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "notification_type IN ('reminder', 'goal_deadline', 'goal_completed', 'system')",
            name='ck_notification_type'
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'sent', 'failed', 'cancelled')",
            name='ck_notification_status'
        ),
        sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_goal_id'), 'notifications', ['goal_id'], unique=False)
    op.create_index(op.f('ix_notifications_notification_type'), 'notifications', ['notification_type'], unique=False)
    op.create_index(op.f('ix_notifications_scheduled_time'), 'notifications', ['scheduled_time'], unique=False)
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)

    # Create notification_settings table
    op.create_table(
        'notification_settings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email_enabled', sa.Boolean(), nullable=False),
        sa.Column('email_reminders', sa.Boolean(), nullable=False),
        sa.Column('email_goal_updates', sa.Boolean(), nullable=False),
        sa.Column('browser_enabled', sa.Boolean(), nullable=False),
        sa.Column('browser_reminders', sa.Boolean(), nullable=False),
        sa.Column('default_reminder_time', sa.String(length=5), nullable=True),
        sa.Column('reminder_before_hours', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_notification_settings_user_id'), 'notification_settings', ['user_id'], unique=True)


def downgrade() -> None:
    # Drop notification_settings table
    op.drop_index(op.f('ix_notification_settings_user_id'), table_name='notification_settings')
    op.drop_table('notification_settings')

    # Drop notifications table
    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_scheduled_time'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_notification_type'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_goal_id'), table_name='notifications')
    op.drop_table('notifications')

    # Remove reminder fields from goals table
    op.drop_column('goals', 'reminder_days_before')
    op.drop_column('goals', 'reminder_time')
    op.drop_column('goals', 'reminder_enabled')
