from datetime import date, datetime, timedelta
from logging import getLogger

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import orm_get_booked_appointment_in_diaposon
from api.api_v1.cabinets.crud import orm_get_cabinet
from api.api_v1.doctors.crud import orm_get_doctor_by_user_id
from api.api_v1.schedules.crud import (
    orm_get_schedule_exception_by_day,
    orm_get_work_schedule_in_day,
)
from api.api_v1.services.crud import orm_get_service
from .schemas import SlotRead

from core.models import WorkSchedule

SLOT_STEP_MINUTES = 15

logger = getLogger(__name__)


async def get_available_slots(
    session: AsyncSession,
    doctor_id: int,
    service_id: int,
    target_date: date,
) -> list[SlotRead]:
    service = await orm_get_service(session=session, service_id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )

    doctor = await orm_get_doctor_by_user_id(session=session, doctor_id=doctor_id)
    if not doctor or not doctor.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found or inactive"
        )

    if service.specialization_id not in [
        s.specialization_id for s in doctor.specializations
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor doesn't have required specialization",
        )

    exception = await orm_get_schedule_exception_by_day(
        session=session, doctor_id=doctor_id, target_date=target_date
    )
    if exception:
        logger.info("Doctor don`t work in this day")
        return []
    weekday = target_date.isoweekday()
    schedule = await orm_get_work_schedule_in_day(
        session=session, doctor_id=doctor_id, weekday=weekday
    )
    if not schedule:
        logger.info(f"Doctor doesn`t have work hours in weekday - {weekday}")
        return []

    cabinet = await orm_get_cabinet(session=session, cabinet_id=schedule.cabinet_id)
    if not cabinet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cabinet not found"
        )
    if cabinet.type != service.cabinet_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cabinet type mismatch"
        )

    slots = _slice_slots(
        target_date=target_date,
        schedule=schedule,
        duration_min=service.duration_min,
        buffer_min=service.buffer_min,
    )

    slots = _exclude_past(slots=slots, target_date=target_date)

    slots = await _exclude_booked(session=session, slots=slots, doctor_id=doctor_id)

    return slots


def _slice_slots(
    target_date: date, schedule: WorkSchedule, duration_min: int, buffer_min: int
) -> list[SlotRead]:
    logger.debug("Start slice slots")
    slots: list[SlotRead] = []
    start = datetime.combine(target_date, schedule.start_time)
    end = datetime.combine(target_date, schedule.end_time)
    total = timedelta(minutes=duration_min + buffer_min)

    while start + total <= end:
        slots.append(
            SlotRead(start=start, end=start + timedelta(minutes=SLOT_STEP_MINUTES))
        )
        start += timedelta(minutes=SLOT_STEP_MINUTES)

    return slots


def _exclude_past(slots: list[SlotRead], target_date: date) -> list[SlotRead]:
    now = datetime.now()
    if target_date < now.date():
        return []
    if target_date > now.date():
        return slots
    return [s for s in slots if s.start > now]


async def _exclude_booked(session: AsyncSession, slots: list[SlotRead], doctor_id: int):
    if not slots:
        return []

    min_start = min(s.start for s in slots)
    max_end = max(s.end for s in slots)

    booked = await orm_get_booked_appointment_in_diaposon(
        session=session,
        doctor_id=doctor_id,
        start_min=min_start,
        end_max=max_end,
    )
    busy_intervals = [(row.starts_at, row.ends_at) for row in booked]

    return [
        slot
        for slot in slots
        if not any(
            slot.start < busy_end and slot.end > busy_start
            for busy_start, busy_end in busy_intervals
        )
    ]
