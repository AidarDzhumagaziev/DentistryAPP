from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base

if TYPE_CHECKING:
    from schedules import WorkSchedule, ScheduleException


class Doctor(Base):
    __tablename__ = "doctors"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), primary_key=True
    )
    experience_years: Mapped[int] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    photo_url: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        nullable=False, default=True, server_default="true"
    )
    specializations: Mapped[list["DoctorSpecialization"]] = relationship(
        back_populates="doctor", cascade="all, delete-orphan"
    )
    work_schedules: Mapped[list["WorkSchedule"]] = relationship(back_populates="doctor")
    schedule_exception: Mapped[list["ScheduleException"]] = relationship(
        back_populates="doctor"
    )


class Specialization(Base):
    __tablename__ = "specializations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    doctors: Mapped[list["DoctorSpecialization"]] = relationship(
        back_populates="specialization"
    )


class DoctorSpecialization(Base):
    __tablename__ = "doctor_specializations"
    __table_args__ = (UniqueConstraint("doctor_id", "specialization_id"),)

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.user_id", ondelete="RESTRICT"),
        primary_key=True,
        nullable=False,
    )
    specialization_id: Mapped[int] = mapped_column(
        ForeignKey("specializations.id", ondelete="RESTRICT"),
        primary_key=True,
        nullable=False,
    )

    doctor: Mapped["Doctor"] = relationship(back_populates="specializations")
    specialization: Mapped["Specialization"] = relationship(back_populates="doctors")
