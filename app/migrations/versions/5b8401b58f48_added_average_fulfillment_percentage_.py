"""Added average_fulfillment_percentage column to Organizations

Revision ID: 5b8401b58f48
Revises: e0f79c6cb735
Create Date: 2024-06-18 20:55:03.268758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b8401b58f48'
down_revision: Union[str, None] = 'e0f79c6cb735'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organizations', sa.Column('average_fulfillment_percentage', sa.Integer(), nullable=True))
    op.drop_column('organizations', 'verified')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organizations', sa.Column('verified', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('organizations', 'average_fulfillment_percentage')
    # ### end Alembic commands ###