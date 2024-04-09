from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Organizations(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[str] = mapped_column()
    organization: Mapped[str] = mapped_column()
    founder: Mapped[str] = mapped_column()
    sphere: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    connected: Mapped[bool] = mapped_column()
    state_mark: Mapped[bool] = mapped_column()
    decoration: Mapped[bool] = mapped_column()
    widgets: Mapped[int] = mapped_column()
    activity: Mapped[int] = mapped_column()
    followers: Mapped[int] = mapped_column()
    weekly_audience: Mapped[int] = mapped_column()
    average_publication_coverage: Mapped[int] = mapped_column()
    total: Mapped[int] = mapped_column()
