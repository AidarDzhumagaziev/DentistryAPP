from typing import TYPE_CHECKING

from datetime import date, time

from sqlalchemy import CheckConstraint, Date, ForeignKey, SmallInteger, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.enums.enums_db import _reason_type_values, ReasonType

from .base import Base
from .mixins import TimeStampMixin

if TYPE_CHECKING:
    from .cabinets import Cabinet
    from .doctors import Doctor


class WorkSchedule(Base, TimeStampMixin):
    __tablename__ = "work_schedules"
    __table_args__ = (
        CheckConstraint(
            "weekday >= 1 AND weekday <= 7",
            name="ck_weekday_between_1_and_7_work_schedules",
        ),
        CheckConstraint(
            "end_time > start_time", name="ck_end_time_more_start_time_work_schedules"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.user_id", ondelete="RESTRICT"), nullable=False
    )
    cabinet_id: Mapped[int] = mapped_column(
        ForeignKey("cabinets.id", ondelete="RESTRICT"), nullable=False
    )
    weekday: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    cabinet: Mapped["Cabinet"] = relationship(back_populates="work_schedules")
    doctor: Mapped["Doctor"] = relationship(back_populates="work_schedules")


class ScheduleException(Base, TimeStampMixin):
    __tablename__ = "schedule_exceptions"
    __table_args__ = (
        CheckConstraint(
            "date_to > date_from", name="ck_date_to_more_date_from_schedule_exceptions"
        ),
        CheckConstraint(
            f"reason IN ({_reason_type_values})",
            name="ck_reason_in_range_schedule_exceptions",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.user_id", ondelete="RESTRICT"), nullable=False
    )
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[ReasonType] = mapped_column(String(50), nullable=False)

    doctor: Mapped["Doctor"] = relationship(back_populates="schedule_exception")


class WaitlistEntry(Base):
    __tablename__ = "waitlist_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.user_id", ondelete="RESTRICT"), nullable=False
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.user_id", ondelete="RESTRICT"), nullable=False
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"), nullable=False
    )
