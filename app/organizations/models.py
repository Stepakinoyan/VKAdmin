from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.statistic.models import Statistic


from typing import List


class Organizations(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[Optional[str]] = mapped_column()
    founder: Mapped[Optional[str]] = mapped_column()
    name: Mapped[Optional[str]] = mapped_column(index=True)
    the_main_state_registration_number: Mapped[Optional[int]] = mapped_column(
        BigInteger
    )
    screen_name: Mapped[Optional[str]] = mapped_column()
    type: Mapped[Optional[str]] = mapped_column()
    city: Mapped[Optional[str]] = mapped_column()
    status: Mapped[Optional[str]] = mapped_column()
    sphere_1: Mapped[Optional[str]] = mapped_column()
    sphere_2: Mapped[Optional[str]] = mapped_column()
    sphere_3: Mapped[Optional[str]] = mapped_column()
    activity: Mapped[Optional[str]] = mapped_column()
    channel_id: Mapped[int] = mapped_column(unique=True)
    members_count: Mapped[int] = mapped_column(default=0)
    has_avatar: Mapped[bool] = mapped_column(default=False)
    has_cover: Mapped[bool] = mapped_column(default=False)
    has_description: Mapped[bool] = mapped_column(default=False)
    has_gos_badge: Mapped[bool] = mapped_column(default=False)
    has_widget: Mapped[Optional[bool]] = mapped_column()
    widget_count: Mapped[Optional[int]] = mapped_column()
    connected: Mapped[Optional[bool]] = mapped_column(default=False)
    url: Mapped[Optional[str]] = mapped_column()
    site: Mapped[Optional[str]] = mapped_column()
    date_added: Mapped[Optional[datetime]] = mapped_column(default=datetime.utcnow)
    posts: Mapped[int] = mapped_column(default=0)
    posts_1d: Mapped[int] = mapped_column(default=0)
    posts_7d: Mapped[int] = mapped_column(default=0)
    posts_30d: Mapped[int] = mapped_column(default=0)
    average_week_fulfillment_percentage: Mapped[int] = mapped_column(default=0)
    average_fulfillment_percentage: Mapped[int] = mapped_column(default=0)
    weekly_audience_reach: Mapped[int] = mapped_column(default=0)

    statistic: Mapped[Optional[List["Statistic"]]] = relationship(
        "Statistic", back_populates="organizations"
    )
