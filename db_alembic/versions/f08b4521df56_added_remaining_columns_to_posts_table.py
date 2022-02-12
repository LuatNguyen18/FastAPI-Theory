"""Added remaining columns to posts table

Revision ID: f08b4521df56
Revises: a9df6cdaf758
Create Date: 2022-02-11 22:13:06.466555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f08b4521df56'
down_revision = 'a9df6cdaf758'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable=False, server_default = sa.text('NOW()')))

    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    
    pass
