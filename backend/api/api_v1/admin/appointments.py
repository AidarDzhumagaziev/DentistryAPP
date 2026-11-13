from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import orm_list_appointments
from api.api_v1.appointments.schemas import AppointmentAdminRead

from common.enums.enums_db import AppointmentStatus
from core.db_helper import db_helper

router = APIRouter(tags=["Admin: Appointments"])


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
