from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()

    sphere: Mapped[Optional[str]] = mapped_column()
