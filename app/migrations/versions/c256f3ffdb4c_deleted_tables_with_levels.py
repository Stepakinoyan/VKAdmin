"""Deleted tables with levels

Revision ID: c256f3ffdb4c
Revises: 2916a6749cce
Create Date: 2024-04-08 20:34:56.935513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c256f3ffdb4c'
down_revision: Union[str, None] = '2916a6749cce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('level_2')
    op.drop_table('level_3')
    op.drop_table('level_1')
    op.add_column('organizations', sa.Column('organization', sa.String(), nullable=False))
    op.add_column('organizations', sa.Column('founder', sa.String(), nullable=False))
    op.add_column('organizations', sa.Column('sphere', sa.String(), nullable=False))
    op.add_column('organizations', sa.Column('address', sa.String(), nullable=False))
    op.add_column('organizations', sa.Column('connected', sa.Boolean(), nullable=False))
    op.add_column('organizations', sa.Column('state_mark', sa.Boolean(), nullable=False))
    op.add_column('organizations', sa.Column('decoration', sa.Boolean(), nullable=False))
    op.add_column('organizations', sa.Column('widgets', sa.Integer(), nullable=False))
    op.add_column('organizations', sa.Column('activity', sa.Integer(), nullable=False))
    op.add_column('organizations', sa.Column('followers', sa.Integer(), nullable=False))
    op.add_column('organizations', sa.Column('weekly_audience', sa.Integer(), nullable=False))
    op.add_column('organizations', sa.Column('average_publication_coverage', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('organizations', 'average_publication_coverage')
    op.drop_column('organizations', 'weekly_audience')
    op.drop_column('organizations', 'followers')
    op.drop_column('organizations', 'activity')
    op.drop_column('organizations', 'widgets')
    op.drop_column('organizations', 'decoration')
    op.drop_column('organizations', 'state_mark')
    op.drop_column('organizations', 'connected')
    op.drop_column('organizations', 'address')
    op.drop_column('organizations', 'sphere')
    op.drop_column('organizations', 'founder')
    op.drop_column('organizations', 'organization')
    op.create_table('level_1',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('organization', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('sphere', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('connected', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('state_mark', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('decoration', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('widgets', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('activity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('followers', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('weekly_audience', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('average_publication_coverage', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='level_1_pkey')
    )
    op.create_table('level_3',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('founder', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('organization', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('sphere', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('connected', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('state_mark', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('decoration', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('widgets', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('activity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('followers', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('weekly_audience', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('average_publication_coverage', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='level_3_pkey')
    )
    op.create_table('level_2',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('organization', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('sphere', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('connected', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('state_mark', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('decoration', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('widgets', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('activity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('followers', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('weekly_audience', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('average_publication_coverage', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='level_2_pkey')
    )
    # ### end Alembic commands ###
