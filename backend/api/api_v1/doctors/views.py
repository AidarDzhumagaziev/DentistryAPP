from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType

from .validation import validation_doctor
from .schemas import DoctorRead, DoctorCreate, DoctorUpdate
from .crud import orm_create_doctor, orm_get_doctor_by_user_id, orm_update_doctor
from .dependecies import doctor_by_id, get_all_doctors

from core.db_helper import db_helper
from core.models import Doctor

logger = getLogger(__name__)

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
    try:
        doctor = await orm_create_doctor(session=session, doctor_create=doctor_create)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Doctor for this user already exists",
        )
    return validation_doctor(doctor)  # type: ignore


@router.get("/", response_model=list[DoctorRead])
async def get_doctors(doctors: list[DoctorRead] = Depends(get_all_doctors)):
    return doctors


@router.get("/{doctor_id}/", response_model=DoctorRead)
async def get_doctor(doctor: Doctor = Depends(doctor_by_id)):
    doctor_read = validation_doctor(doctor)
    return doctor_read


@router.put(
    "/{doctor_id}/",
    response_model=DoctorRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_doctor(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor_update: DoctorUpdate,
    doctor: Doctor = Depends(doctor_by_id),
):
    try:
        updated_doctor = await orm_update_doctor(
            session=session, doctor=doctor, doctor_update=doctor_update
        )
    except IntegrityError:
        logger.error(f"Doctor {doctor.user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Doctor not found"
        )
    return validation_doctor(updated_doctor)  # type: ignore
