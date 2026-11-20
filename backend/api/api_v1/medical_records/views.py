from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import orm_get_appointment
from api.api_v1.appointments.validation import _ensure_owns_doctor
from api.api_v1.auth.validation import require_role
from common.enums.enums_db import AppointmentStatus, RoleType

from core.db_helper import db_helper
from core.models import User

from .crud import orm_create_medical_record, orm_get_medical_record_by_appointment_id
from .schemas import MedicalRecordCreate, MedicalRecordRead

router = APIRouter(tags=["Medical Records"])


@router.post(
    "/",
    response_model=MedicalRecordRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_medical_record(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    record_create: MedicalRecordCreate,
    current_user: User = Depends(require_role(RoleType.DOCTOR)),
):
    medical_record = await orm_get_medical_record_by_appointment_id(
        session=session, appointment_id=record_create.appointment_id
    )
    if medical_record is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Appointment already has medical record",
        )
    appointment = await orm_get_appointment(
        session=session, appointment_id=record_create.appointment_id
    )
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get appointment",
        )
    await _ensure_owns_doctor(appointment=appointment, current_user=current_user)

    if appointment.status != AppointmentStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Appointment has not completed yet",
        )

    medical_record = await orm_create_medical_record(
        session=session, medical_record_create=record_create
    )
    return medical_record
