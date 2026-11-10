from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Path, status, Depends, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.appointments.crud import orm_get_appointment_by_doctor_id
from api.api_v1.appointments.schemas import AppointmentRead
from api.api_v1.auth.validation import require_role
from api.api_v1.schedules.crud import (
    orm_get_schedule_exceptions_by_doctor_id,
    orm_get_work_schedules,
)
from api.api_v1.schedules.schemas import ScheduleExceptionRead, WorkScheduleRead
from common.enums.enums_db import RoleType

from .validation import validation_doctor
from .schemas import DoctorRead, DoctorCreate, DoctorUpdate, DoctorUpdatePartial
from .crud import (
    orm_create_doctor,
    orm_update_doctor,
    orm_delete_doctor,
)
from .dependecies import doctor_by_id, get_all_doctors

from core.db_helper import db_helper
from core.models import Doctor

logger = getLogger(__name__)

router = APIRouter(tags=["Doctors"])


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


@router.get("/{doctor_id}/work_schedules", response_model=list[WorkScheduleRead])
async def get_all_the_work_schedules(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor_id: Annotated[int, Path],
):
    return await orm_get_work_schedules(session=session, doctor_id=doctor_id)


@router.get(
    "/{doctor_id}/schedules_exception", response_model=list[ScheduleExceptionRead]
)
async def get_all_the_schedule_exception(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor_id: Annotated[int, Path],
):
    return await orm_get_schedule_exceptions_by_doctor_id(
        session=session, doctor_id=doctor_id
    )


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


@router.patch(
    "/{doctor_id}/",
    response_model=DoctorRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_doctor_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor_update: DoctorUpdatePartial,
    doctor: Doctor = Depends(doctor_by_id),
):
    try:
        updated_doctor = await orm_update_doctor(
            session=session, doctor=doctor, doctor_update=doctor_update, partial=True
        )
    except IntegrityError:
        logger.error(f"Doctor {doctor.user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Doctor not found"
        )
    return validation_doctor(updated_doctor)  # type: ignore


@router.delete(
    "/{doctor_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def delete_doctor(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor: Doctor = Depends(doctor_by_id),
):
    await orm_delete_doctor(session=session, doctor=doctor)


@router.get(
    "/{doctor_id}/appointments",
    response_model=list[AppointmentRead],
    dependencies=[Depends(require_role(RoleType.ADMIN, RoleType.DOCTOR))],
)
async def get_appointments(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor: Doctor = Depends(doctor_by_id),
):
    appointments = await orm_get_appointment_by_doctor_id(
        session=session, doctor_id=doctor.user_id
    )
    return appointments
