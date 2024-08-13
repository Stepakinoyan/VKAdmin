from datetime import date, datetime
from typing import Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.organizations.models import Organizations


class Statistic(Base):
    __tablename__ = "statistic"

    date_id: Mapped[str] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    date_added: Mapped[date] = mapped_column(default=datetime.utcnow().date)
    members_count: Mapped[int] = mapped_column(default=0)
    fulfillment_percentage: Mapped[int] = mapped_column()

    activity: Mapped[Optional[dict]] = mapped_column(JSON)

    organizations: Mapped["Organizations"] = relationship(
        "Organizations", back_populates="statistic"
    )
