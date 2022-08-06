"""add last few columns to posts table

Revision ID: 3956101ff83c
Revises: 0d96067cb24b
Create Date: 2022-08-06 16:13:49.909997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3956101ff83c'
down_revision = '0d96067cb24b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
