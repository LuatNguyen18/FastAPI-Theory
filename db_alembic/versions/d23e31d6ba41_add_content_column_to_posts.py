"""Add content column to posts

Revision ID: d23e31d6ba41
Revises: a16ea965a968
Create Date: 2022-02-10 22:36:24.034817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd23e31d6ba41'
down_revision = 'a16ea965a968'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
