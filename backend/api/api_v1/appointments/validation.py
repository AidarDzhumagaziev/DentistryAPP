from logging import getLogger

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import (
    orm_get_appointments_by_patient_id_and_datetime,
    orm_get_conflict_between_appointment,
)
from api.api_v1.doctors.crud import orm_get_doctor
from api.api_v1.schedules.crud import (
    orm_get_schedule_exception_by_day,
    orm_get_work_schedule_by_datetime,
)
from api.api_v1.services.crud import orm_get_service

from common.enums.enums_db import AppointmentStatus
from core.models import Doctor, Service, Cabinet, Appointment, User, WorkSchedule

from .schemas import AppointmentCreate

logger = getLogger(__name__)


async def validate_appointment(
    session: AsyncSession, appointment_create: AppointmentCreate, user: User
) -> WorkSchedule:
    doctor, service = await _get_appointment_entities(
        session=session, appointment_create=appointment_create
    )
    schedule = await resolve_work_schedule(
        session=session, appointment_create=appointment_create
    )
    _check_appointment_compatibility(
        doctor=doctor, service=service, cabinet=schedule.cabinet
    )
    await is_slot_available(
        session=session,
        appointment_create=appointment_create,
        work_schedule=schedule,
        patient_id=user.id,
    )
    return schedule


async def resolve_work_schedule(
    session: AsyncSession, appointment_create: AppointmentCreate
) -> WorkSchedule:
    schedule = await orm_get_work_schedule_by_datetime(
        session=session,
        doctor_id=appointment_create.doctor_id,
        isoweekday=appointment_create.starts_at.isoweekday(),
        start_time=appointment_create.starts_at.time(),
        end_time=appointment_create.ends_at.time(),
    )
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Doctor is now working at this time",
        )
    return schedule


async def _get_appointment_entities(
    session: AsyncSession, appointment_create: AppointmentCreate
) -> tuple[Doctor, Service]:
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
    return doctor, service


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
    work_schedule: WorkSchedule,
    patient_id: int,
):
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
    patient_conflict = await orm_get_appointments_by_patient_id_and_datetime(
        session=session,
        patient_id=patient_id,
        start=appointment_create.starts_at,
        end=appointment_create.ends_at,
    )
    if patient_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Patient has appointment in this diaposon",
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
