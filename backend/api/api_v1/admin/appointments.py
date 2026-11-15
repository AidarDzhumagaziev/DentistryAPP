from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import (
    orm_create_appointment,
    orm_get_appointment,
    orm_list_appointments,
)
from api.api_v1.appointments.dependencies import appointment_by_id
from api.api_v1.appointments.schemas import AppointmentAdminCreate, AppointmentAdminRead

from api.api_v1.appointments.validation import validate_appointment
from api.api_v1.patients.crud import orm_get_patient
from common.enums.enums_db import AppointmentStatus
from core.db_helper import db_helper
from core.models import Appointment

router = APIRouter(tags=["Admin: Appointments"])


@router.post(
    "/", response_model=AppointmentAdminRead, status_code=status.HTTP_201_CREATED
)
async def admin_create_appointment(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment_create: AppointmentAdminCreate,
):
    patient = await orm_get_patient(
        session=session, user_id=appointment_create.patient_id
    )
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    schedule = await validate_appointment(
        session=session, appointment_create=appointment_create
    )

    appointment = await orm_create_appointment(
        session=session,
        appointment_create=appointment_create,
        patient_id=appointment_create.patient_id,
        cabinet_id=schedule.cabinet_id,
    )

    return await orm_get_appointment(session=session, appointment_id=appointment.id)


@router.get("/", response_model=list[AppointmentAdminRead])
async def get_appointments(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    patient_id: int | None = None,
    doctor_id: int | None = None,
    status: AppointmentStatus | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = 50,
    offset: int = 0,
):
    return await orm_list_appointments(
        session=session,
        patient_id=patient_id,
        doctor_id=doctor_id,
        status=status,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )


@router.patch("/{appointment_id}/reassign", response_model=AppointmentAdminRead)
async def reassign_doctor(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor_id: Annotated[int, Path],
    appointment: Appointment = Depends(appointment_by_id),
):
    appointment.doctor_id = doctor_id
    await session.commit()
    return appointment
