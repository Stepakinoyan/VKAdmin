from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.organizations.models import Organizations


class Statistic(Base):
    __tablename__ = "statistic"

    date_id: Mapped[str] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    date_added: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    members_count: Mapped[int] = mapped_column()
    fulfillment_percentage: Mapped[int] = mapped_column()

    organizations: Mapped["Organizations"] = relationship(
        "Organizations", back_populates="statistic"
    )
