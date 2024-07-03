from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.vk.models import Statistic


class Organizations(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[Optional[str]] = mapped_column()
    founder: Mapped[Optional[str]] = mapped_column()
    name: Mapped[Optional[str]] = mapped_column()
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
    channel_id: Mapped[Optional[int]] = mapped_column(unique=True)
    has_avatar: Mapped[Optional[bool]] = mapped_column()
    has_cover: Mapped[Optional[bool]] = mapped_column()
    has_description: Mapped[Optional[bool]] = mapped_column()
    has_gos_badge: Mapped[Optional[bool]] = mapped_column()
    has_widget: Mapped[Optional[bool]] = mapped_column()
    widget_count: Mapped[Optional[int]] = mapped_column()
    members_count: Mapped[Optional[int]] = mapped_column()
    url: Mapped[Optional[str]] = mapped_column()
    site: Mapped[Optional[str]] = mapped_column()
    date_added: Mapped[Optional[datetime]] = mapped_column(default=datetime.utcnow)
    posts: Mapped[Optional[int]] = mapped_column()
    posts_1d: Mapped[Optional[int]] = mapped_column()
    posts_7d: Mapped[Optional[int]] = mapped_column()
    posts_30d: Mapped[Optional[int]] = mapped_column()
    views_7d: Mapped[Optional[int]] = mapped_column(default=0)
    post_date: Mapped[Optional[datetime]] = mapped_column()

    statistic: Mapped[Optional[list["Statistic"]]] = relationship(
        "Statistic", back_populates="organizations"
    )

    average_week_fulfillment_percentage: Mapped[Optional[int]] = mapped_column(default=0)
    average_fulfillment_percentage: Mapped[Optional[int]] = mapped_column(default=0)
