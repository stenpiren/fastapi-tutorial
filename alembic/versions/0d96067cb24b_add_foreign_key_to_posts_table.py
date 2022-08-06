"""add foreign-key  to posts table

Revision ID: 0d96067cb24b
Revises: cac8dc0b91c2
Create Date: 2022-08-06 16:08:59.514485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d96067cb24b'
down_revision = 'cac8dc0b91c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
