"""Created users table

Revision ID: c0b1d8710e65
Revises: d23e31d6ba41
Create Date: 2022-02-10 22:38:18.474609

"""
from http import server
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0b1d8710e65'
down_revision = 'd23e31d6ba41'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))

    pass


def downgrade():
    op.drop_table('users')
    pass
