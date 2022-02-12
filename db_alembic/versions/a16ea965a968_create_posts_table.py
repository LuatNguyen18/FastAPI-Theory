"""Create posts table

Revision ID: a16ea965a968
Revises: 
Create Date: 2022-02-10 22:28:21.033976

"""
from logging import NullHandler
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a16ea965a968'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
