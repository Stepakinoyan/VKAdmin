from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger
from app.database import Base

if TYPE_CHECKING:
    from app.vk.models import Account


class Organizations(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[Optional[str]] = mapped_column()
    founder: Mapped[Optional[str]] = mapped_column()
    name: Mapped[Optional[str]] = mapped_column()
    reason: Mapped[Optional[str]] = mapped_column()
    the_main_state_registration_number: Mapped[Optional[int]] = mapped_column(
        BigInteger
    )
    sphere_1: Mapped[Optional[str]] = mapped_column()
    sphere_2: Mapped[Optional[str]] = mapped_column()
    sphere_3: Mapped[Optional[str]] = mapped_column()
    status: Mapped[Optional[str]] = mapped_column()
    channel_id: Mapped[Optional[int]] = mapped_column(unique=True)
    url: Mapped[Optional[str]] = mapped_column()
    address: Mapped[Optional[str]] = mapped_column()
    connected: Mapped[Optional[str]] = mapped_column()
    state_mark: Mapped[Optional[bool]] = mapped_column()
    decoration: Mapped[Optional[str]] = mapped_column()
    widgets: Mapped[Optional[str]] = mapped_column()
    activity: Mapped[Optional[str]] = mapped_column()
    followers: Mapped[Optional[str]] = mapped_column()
    weekly_audience: Mapped[Optional[str]] = mapped_column()
    average_publication_coverage: Mapped[Optional[str]] = mapped_column()

    account: Mapped[Optional["Account"]] = relationship(
        "Account", back_populates="organizations", uselist=False
    )
