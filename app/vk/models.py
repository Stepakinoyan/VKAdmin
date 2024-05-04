from datetime import datetime
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    screen_name: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    activity: Mapped[str] = mapped_column()
    verified: Mapped[bool] = mapped_column()
    has_avatar: Mapped[bool] = mapped_column()
    has_cover: Mapped[bool] = mapped_column()
    has_description: Mapped[bool] = mapped_column()
    has_gos_badge: Mapped[bool] = mapped_column()
    has_widget: Mapped[bool] = mapped_column()
    widget_count: Mapped[int] = mapped_column()
    members_count: Mapped[int] = mapped_column()
    site: Mapped[str] = mapped_column()
    date_added: Mapped[datetime] = mapped_column()  # default=datetime.utcnow
    posts: Mapped[int] = mapped_column()
    posts_1d: Mapped[int] = mapped_column()
    posts_7d: Mapped[int] = mapped_column()
    posts_30d: Mapped[int] = mapped_column()
    post_date: Mapped[datetime] = mapped_column()


class Statistic(Base):
    __tablename__ = "statistic"

    date_id: Mapped[str] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    date_added: Mapped[datetime] = mapped_column()  # default=datetime.utcnow
    members_count: Mapped[int] = mapped_column()
