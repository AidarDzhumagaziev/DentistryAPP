from logging import getLogger
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import (
    orm_create_appointment,
    orm_get_conflict_between_appointment,
)
from api.api_v1.cabinets.crud import orm_get_cabinet
from api.api_v1.doctors.crud import orm_get_doctor
from api.api_v1.services.crud import orm_get_service
from core.db_helper import db_helper

from .schemas import AppointmentCreate

logger = getLogger(__name__)


async def validate_appointment_create(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment_create: AppointmentCreate,
):
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
    conflict = await orm_get_conflict_between_appointment(
        session=session, appointment=appointment_create
    )
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Slot is already booked"
        )
    return await orm_create_appointment(
        session=session, appointment_create=appointment_create
    )
