"""add daily review screen time and steps fields

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2025-11-15 04:41:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2c3d4e5f6g7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add screen_time_minutes and steps columns to daily_reviews table."""
    op.add_column('daily_reviews', sa.Column('screen_time_minutes', sa.Integer(), nullable=True))
    op.add_column('daily_reviews', sa.Column('steps', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Remove screen_time_minutes and steps columns from daily_reviews table."""
    op.drop_column('daily_reviews', 'steps')
    op.drop_column('daily_reviews', 'screen_time_minutes')
