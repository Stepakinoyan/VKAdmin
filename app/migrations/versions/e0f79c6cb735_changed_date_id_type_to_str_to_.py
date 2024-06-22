"""Changed date_id type to str to statistic table back

Revision ID: e0f79c6cb735
Revises:
Create Date: 2024-06-06 16:25:43.033330

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e0f79c6cb735"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("level", sa.String(), nullable=True),
        sa.Column("founder", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("the_main_state_registration_number", sa.BigInteger(), nullable=True),
        sa.Column("screen_name", sa.String(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("sphere_1", sa.String(), nullable=True),
        sa.Column("sphere_2", sa.String(), nullable=True),
        sa.Column("sphere_3", sa.String(), nullable=True),
        sa.Column("activity", sa.String(), nullable=True),
        sa.Column("verified", sa.Boolean(), nullable=True),
        sa.Column("channel_id", sa.Integer(), nullable=True),
        sa.Column("has_avatar", sa.Boolean(), nullable=True),
        sa.Column("has_cover", sa.Boolean(), nullable=True),
        sa.Column("has_description", sa.Boolean(), nullable=True),
        sa.Column("has_gos_badge", sa.Boolean(), nullable=True),
        sa.Column("has_widget", sa.Boolean(), nullable=True),
        sa.Column("widget_count", sa.Integer(), nullable=True),
        sa.Column("members_count", sa.Integer(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("site", sa.String(), nullable=True),
        sa.Column("date_added", sa.DateTime(), nullable=True),
        sa.Column("posts", sa.Integer(), nullable=True),
        sa.Column("posts_1d", sa.Integer(), nullable=True),
        sa.Column("posts_7d", sa.Integer(), nullable=True),
        sa.Column("posts_30d", sa.Integer(), nullable=True),
        sa.Column("post_date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("channel_id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "statistic",
        sa.Column("date_id", sa.String(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("date_added", sa.DateTime(), nullable=False),
        sa.Column("members_count", sa.Integer(), nullable=False),
        sa.Column("fulfillment_percentage", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
        ),
        sa.PrimaryKeyConstraint("date_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("statistic")
    op.drop_table("users")
    op.drop_table("organizations")
    # ### end Alembic commands ###
