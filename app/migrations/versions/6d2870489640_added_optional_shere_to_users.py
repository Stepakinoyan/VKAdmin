"""Added optional shere to users

Revision ID: 6d2870489640
Revises: 36f377b91807
Create Date: 2024-08-26 14:42:16.074261

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6d2870489640"
down_revision: Union[str, None] = "36f377b91807"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "sphere", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "sphere", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###