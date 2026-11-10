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

from .schemas import AppointmentCreate

logger = getLogger(__name__)


async def validate_appointment(
    session: AsyncSession,
    appointment_create: AppointmentCreate,
) -> None:
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
    if service.specialization_id not in {
        s.specialization_id for s in doctor.specializations
    }:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Doctor does not provide this service",
        )
    cabinet = await orm_get_cabinet(
        session=session, cabinet_id=appointment_create.cabinet_id
    )
    if not cabinet:
        logger.warning(f"Cabinet {appointment_create.cabinet_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cabinet not found"
        )
    if cabinet.type != service.cabinet_type:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="The service cannot be provided in this cabinet",
        )
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
