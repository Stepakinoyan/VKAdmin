"""Added default params to date_added columns

Revision ID: 84368fc5ee6f
Revises: fccd361b8e03
Create Date: 2024-05-13 20:30:47.537639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84368fc5ee6f'
down_revision: Union[str, None] = 'fccd361b8e03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###