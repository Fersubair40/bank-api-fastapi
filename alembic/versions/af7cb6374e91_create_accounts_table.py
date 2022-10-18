"""create accounts table

Revision ID: af7cb6374e91
Revises: ec1a28325473
Create Date: 2022-07-29 15:24:25.085537

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'af7cb6374e91'
down_revision = 'ec1a28325473'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('available_balance', sa.DECIMAL(), nullable=False),
    sa.Column('active', sa.Boolean(), server_default='false', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accounts')
    # ### end Alembic commands ###
