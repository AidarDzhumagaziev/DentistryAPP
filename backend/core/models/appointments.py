from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.enums.enums_db import AppointmentStatus, _appointment_status_values

from .base import Base
from .mixins import CreatedAtMixin, TimeStampMixin

if TYPE_CHECKING:
    from .doctors import Doctor
    from .patients import Patient
    from .services import Service
    from .cabinets import Cabinet


class Appointment(Base, CreatedAtMixin):
    __tablename__ = "appointments"
    __table_args__ = (
        CheckConstraint(
            "ends_at > starts_at", name="ck_end_at_more_start_at_appointments"
        ),
        CheckConstraint(
            f"status IN ({_appointment_status_values})",
            name="ck_status_in_range_appointments",
        ),
    )

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.user_id", ondelete="RESTRICT"), nullable=False
    )
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.user_id", ondelete="RESTRICT"), nullable=False
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"), nullable=False
    )
    cabinet_id: Mapped[int] = mapped_column(
        ForeignKey("cabinets.id", ondelete="RESTRICT"), nullable=False
    )
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(
        String(50),
        default=AppointmentStatus.SCHEDULED.value,
        server_default=AppointmentStatus.SCHEDULED.value,
        nullable=False,
    )

    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")
    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    service: Mapped["Service"] = relationship(back_populates="appointments")
    cabinet: Mapped["Cabinet"] = relationship(back_populates="appointments")


class MedicalRecord(Base, TimeStampMixin):
    __tablename__ = "medical_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id"), unique=True
    )

    complaints: Mapped[str | None]
    objective_findings: Mapped[str | None]
    diagnosis: Mapped[str | None]
    treatment_plan: Mapped[str | None]
