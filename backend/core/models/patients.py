from typing import TYPE_CHECKING

from datetime import date

from sqlalchemy import Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import TimeStampMixin

if TYPE_CHECKING:
    from .appointments import Appointment
    from .users import User


class Patient(Base, TimeStampMixin):
    __tablename__ = "patients"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), primary_key=True
    )
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    allergies: Mapped[str] = mapped_column(Text, nullable=False)
    chronic_diseas: Mapped[str] = mapped_column(Text, nullable=False)
    no_show_count: Mapped[int] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="patient_profile")
    appointments: Mapped["Appointment"] = relationship(back_populates="patient")
