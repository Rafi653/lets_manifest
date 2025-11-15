"""add life goals support with milestones

Revision ID: c3d4e5f6g7h8
Revises: b2c3d4e5f6g7
Create Date: 2025-11-15 05:25:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'c3d4e5f6g7h8'
down_revision = 'b2c3d4e5f6g7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add life goal support and milestones table."""
    
    # Drop existing constraints
    op.drop_constraint('ck_goal_type', 'goals', type_='check')
    op.drop_constraint('ck_goal_status', 'goals', type_='check')
    
    # Make start_date and end_date nullable for life goals
    op.alter_column('goals', 'start_date',
                    existing_type=sa.DATE(),
                    nullable=True)
    op.alter_column('goals', 'end_date',
                    existing_type=sa.DATE(),
                    nullable=True)
    
    # Add updated constraints with life_goal type and in_progress status
    op.create_check_constraint(
        'ck_goal_type',
        'goals',
        "goal_type IN ('daily', 'weekly', 'monthly', 'yearly', 'life_goal')"
    )
    op.create_check_constraint(
        'ck_goal_status',
        'goals',
        "status IN ('active', 'completed', 'cancelled', 'paused', 'in_progress')"
    )
    
    # Create goal_milestones table
    op.create_table(
        'goal_milestones',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('goal_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('target_date', sa.Date(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.CheckConstraint("status IN ('pending', 'in_progress', 'completed', 'skipped')", name='ck_milestone_status'),
        sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_goal_milestones_goal_id'), 'goal_milestones', ['goal_id'], unique=False)


def downgrade() -> None:
    """Remove life goal support and milestones table."""
    
    # Drop milestones table
    op.drop_index(op.f('ix_goal_milestones_goal_id'), table_name='goal_milestones')
    op.drop_table('goal_milestones')
    
    # Drop updated constraints
    op.drop_constraint('ck_goal_type', 'goals', type_='check')
    op.drop_constraint('ck_goal_status', 'goals', type_='check')
    
    # Restore original constraints
    op.create_check_constraint(
        'ck_goal_type',
        'goals',
        "goal_type IN ('daily', 'weekly', 'monthly', 'yearly')"
    )
    op.create_check_constraint(
        'ck_goal_status',
        'goals',
        "status IN ('active', 'completed', 'cancelled', 'paused')"
    )
    
    # Make dates non-nullable again
    op.alter_column('goals', 'start_date',
                    existing_type=sa.DATE(),
                    nullable=False)
    op.alter_column('goals', 'end_date',
                    existing_type=sa.DATE(),
                    nullable=False)
