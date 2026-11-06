from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import require_role
from api.api_v1.specializations.schemas import SpecializationRead
from api.api_v1.users.schemas import UserRead
from common.enums.enums_db import RoleType

from .schemas import DoctorRead, DoctorCreate
from .crud import orm_create_doctor, orm_get_doctor_by_user_id, orm_get_doctors
from .dependecies import get_all_doctors

from core.db_helper import db_helper

router = APIRouter()


@router.post(
    "/",
    response_model=DoctorRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def create_doctor(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor_create: DoctorCreate,
):
    doctor = await orm_get_doctor_by_user_id(
        session=session, user_id=doctor_create.user_id
    )
    if doctor is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Doctor {doctor.user.full_name} already exists",
        )
    return await orm_create_doctor(session=session, doctor_create=doctor_create)


@router.get("/", response_model=list[DoctorRead])
async def get_doctors(doctors: list[DoctorRead] = Depends(get_all_doctors)):
    return doctors
