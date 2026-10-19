from typing import TYPE_CHECKING

from datetime import date, time

from sqlalchemy import CheckConstraint, Date, ForeignKey, SmallInteger, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.enums.enums_db import _reason_type_values, ReasonType

from base import Base

if TYPE_CHECKING:
    from cabinets import Cabinet
    from doctors import Doctor


class WorkSchedule(Base):
    __tablename__ = "work_schedules"
    __table_args__ = (
        CheckConstraint("weekday >= 1 AND weekday <= 7"),
        CheckConstraint("end_time > start_time"),
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


class ScheduleException(Base):
    __tablename__ = "schedule_exceptions"
    __table_args__ = (
        CheckConstraint("date_to > date_from"),
        CheckConstraint(f"reason IN ({_reason_type_values})"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.user_id", ondelete="RESTRICT"), nullable=False
    )
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[ReasonType] = mapped_column(String(50), nullable=False)

    doctor: Mapped["Doctor"] = relationship(back_populates="schedule_exception")
