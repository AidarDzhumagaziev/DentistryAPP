from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType

from core.db_helper import db_helper

from .crud import orm_create_patient, orm_get_patient
from .schemas import PatientCreate, PatientRead

router = APIRouter(tags=["Patients"])


@router.post(
    "/",
    response_model=PatientRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def create_patient(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    patient_create: PatientCreate,
):
    patient = await orm_get_patient(session=session, user_id=patient_create.user_id)
    if patient is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has patient profile",
        )
    return await orm_create_patient(session=session, patient_create=patient_create)
