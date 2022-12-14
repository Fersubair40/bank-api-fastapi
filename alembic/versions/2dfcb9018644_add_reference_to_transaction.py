"""add reference to transaction

Revision ID: 2dfcb9018644
Revises: 9912401f2756
Create Date: 2022-10-20 07:36:21.350728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dfcb9018644'
down_revision = '9912401f2756'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('reference', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'reference')
    # ### end Alembic commands ###
