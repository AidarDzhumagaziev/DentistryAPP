from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import orm_create_appointment
from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType

from core.db_helper import db_helper
from core.models import Appointment

from .dependencies import validate_appointment
from .schemas import AppointmentCreate, AppointmentRead

logger = getLogger(__name__)

router = APIRouter(tags=["Appointments"])


@router.post(
    "/",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.ADMIN, RoleType.DOCTOR))],
)
async def create_appointment(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment_create: AppointmentCreate,
):
    await validate_appointment(session=session, appointment_create=appointment_create)
    return await orm_create_appointment(
        session=session, appointment_create=appointment_create
    )
