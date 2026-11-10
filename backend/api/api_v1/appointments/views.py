from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import orm_create_appointment, orm_get_appointment
from api.api_v1.auth.validation import get_current_auth_user, require_role
from common.enums.enums_db import RoleType

from core.db_helper import db_helper
from core.models import Appointment, User

from .dependencies import validate_appointment
from .schemas import AppointmentCreate, AppointmentRead

logger = getLogger(__name__)

router = APIRouter(tags=["Appointments"])


@router.post(
    "/",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.PATIENT))],
)
async def create_appointment(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment_create: AppointmentCreate,
    current_user: User = Depends(get_current_auth_user),
):
    await validate_appointment(
        session=session,
        appointment_create=appointment_create,
    )
    return await orm_create_appointment(
        session=session,
        appointment_create=appointment_create,
        patient_id=current_user.id,
    )


@router.get(
    "/{appointment_id}/",
    response_model=AppointmentRead,
    dependencies=[Depends(require_role(RoleType.ADMIN, RoleType.DOCTOR))],
)
async def get_appointment(
    appointment_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await orm_get_appointment(session=session, appointment_id=appointment_id)
