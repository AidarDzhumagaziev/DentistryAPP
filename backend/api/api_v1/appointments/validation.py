from logging import getLogger

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import orm_get_conflict_between_appointment
from api.api_v1.cabinets.crud import orm_get_cabinet
from api.api_v1.doctors.crud import orm_get_doctor
from api.api_v1.schedules.crud import (
    orm_get_schedule_exception_by_day,
    orm_get_work_schedule_in_day,
)
from api.api_v1.services.crud import orm_get_service

from common.enums.enums_db import AppointmentStatus
from core.models import Doctor, Service, Cabinet
from core.models import Appointment, User

from .schemas import AppointmentCreate

logger = getLogger(__name__)


async def validate_appointment(
    session: AsyncSession,
    appointment_create: AppointmentCreate,
) -> None:
    doctor, service, cabinet = await _get_appointment_entities(
        session=session, appointment_create=appointment_create
    )
    _check_appointment_compatibility(doctor=doctor, service=service, cabinet=cabinet)
    await is_slot_available(session=session, appointment_create=appointment_create)


async def _get_appointment_entities(
    session: AsyncSession, appointment_create: AppointmentCreate
) -> tuple[Doctor, Service, Cabinet]:
    doctor = await orm_get_doctor(
        session=session, doctor_id=appointment_create.doctor_id
    )
    if not doctor:
        logger.warning(f"Doctor {appointment_create.doctor_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )
    service = await orm_get_service(
        session=session, service_id=appointment_create.service_id
    )
    if not service:
        logger.warning(f"Service {appointment_create.service_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    cabinet = await orm_get_cabinet(
        session=session, cabinet_id=appointment_create.cabinet_id
    )
    if not cabinet:
        logger.warning(f"Cabinet {appointment_create.cabinet_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cabinet not found"
        )
    return doctor, service, cabinet


def _check_appointment_compatibility(
    doctor: Doctor, service: Service, cabinet: Cabinet
) -> None:
    if service.specialization_id not in {
        s.specialization_id for s in doctor.specializations
    }:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Doctor does not provide this service",
        )
    if cabinet.type != service.cabinet_type:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="The service cannot be provided in this cabinet",
        )


async def is_slot_available(
    session: AsyncSession,
    appointment_create: AppointmentCreate,
):
    work_schedule = await orm_get_work_schedule_in_day(
        session=session,
        doctor_id=appointment_create.doctor_id,
        weekday=appointment_create.starts_at.isoweekday(),
    )
    if not work_schedule:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Doctor is not working at this day",
        )
    if (
        work_schedule.start_time > appointment_create.starts_at.time()
        or work_schedule.end_time < appointment_create.ends_at.time()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Slot is outside doctor`s work schedule",
        )
    schedule_exception = await orm_get_schedule_exception_by_day(
        session=session,
        doctor_id=appointment_create.doctor_id,
        target_date=appointment_create.starts_at.date(),
    )
    if schedule_exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Doctor is unavailable at this time",
        )
    conflict = await orm_get_conflict_between_appointment(
        session=session, appointment=appointment_create
    )
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Slot is already booked"
        )


def check_valid_status_for_cancelled(appointment: Appointment):
    if (
        appointment.status == AppointmentStatus.COMPLETED
        or appointment.status == AppointmentStatus.NO_SHOW
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel appointment in status {appointment.status!r}",
        )


def check_valid_status_for_confirmed(appointment: Appointment):
    if (
        appointment.status == AppointmentStatus.CANCELLED
        or appointment.status == AppointmentStatus.NO_SHOW
        or appointment.status == AppointmentStatus.COMPLETED
        or appointment.status == AppointmentStatus.CONFIRMED
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot confirm appointment in status {appointment.status!r}",
        )


def check_valid_status_for_completed(appointment: Appointment):
    if (
        appointment.status == AppointmentStatus.CANCELLED
        or appointment.status == AppointmentStatus.NO_SHOW
        or appointment.status == AppointmentStatus.COMPLETED
        or appointment.status == AppointmentStatus.SCHEDULED
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot confirm appointment in status {appointment.status!r}",
        )


def check_valid_status_for_set_no_show(appointment: Appointment):
    if (
        appointment.status == AppointmentStatus.CANCELLED
        or appointment.status == AppointmentStatus.COMPLETED
        or appointment.status == AppointmentStatus.SCHEDULED
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot confirm appointment in status {appointment.status!r}",
        )


async def _ensure_owns_doctor(appointment: Appointment, current_user: User):
    if appointment.doctor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not your appointment"
        )


async def _ensure_owns_patient(appointment: Appointment, current_user: User):
    if appointment.patient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not your appointment"
        )
