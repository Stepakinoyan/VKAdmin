from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.organizations.models import Organizations


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.channel_id"), unique=True
    )
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
    date_added: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    posts: Mapped[int] = mapped_column()
    posts_1d: Mapped[int] = mapped_column()
    posts_7d: Mapped[int] = mapped_column()
    posts_30d: Mapped[int] = mapped_column()
    post_date: Mapped[datetime] = mapped_column()

    organizations: Mapped["Organizations"] = relationship(
        "Organizations", back_populates="account"
    )
    statistic: Mapped[list["Statistic"]] = relationship(
        "Statistic", back_populates="account"
    )


class Statistic(Base):
    __tablename__ = "statistic"

    date_id: Mapped[str] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    date_added: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    members_count: Mapped[int] = mapped_column()
    fulfillment_percentage: Mapped[int] = mapped_column()

    account: Mapped["Account"] = relationship("Account", back_populates="statistic")
