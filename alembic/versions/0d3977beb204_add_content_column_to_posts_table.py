"""add content column to posts table

Revision ID: 0d3977beb204
Revises: f64840ffb002
Create Date: 2022-08-06 15:58:13.681722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d3977beb204'
down_revision = 'f64840ffb002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
