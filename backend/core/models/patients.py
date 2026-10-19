from datetime import date

from sqlalchemy import Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Patient(Base):
    __tablename__ = "patients"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), primary_key=True
    )
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    allergies: Mapped[str] = mapped_column(Text, nullable=False)
    chronic_diseas: Mapped[str] = mapped_column(Text, nullable=False)
    no_show_count: Mapped[int] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
