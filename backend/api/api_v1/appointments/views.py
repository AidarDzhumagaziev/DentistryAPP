from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import get_current_auth_user, require_role
from api.api_v1.schedules.crud import orm_get_work_schedule_by_datetime
from common.enums.enums_db import AppointmentStatus, RoleType

from core.db_helper import db_helper
from core.models import Appointment, User

from .crud import (
    orm_create_appointment,
    orm_get_appointment,
    orm_update_appointment_status,
    orm_list_appointments,
)
from .dependencies import appointment_by_id
from .validation import (
    _ensure_owns_doctor,
    _ensure_owns_patient,
    check_valid_status_for_cancelled,
    validate_appointment,
    check_valid_status_for_confirmed,
    check_valid_status_for_completed,
    check_valid_status_for_set_no_show,
)
from .schemas import (
    AppointmentAdminRead,
    AppointmentCreate,
    AppointmentDoctorRead,
    AppointmentPatientRead,
    AppointmentUpdate,
)

logger = getLogger(__name__)

router = APIRouter(tags=["Appointments"])


@router.post(
    "/",
    response_model=AppointmentPatientRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.PATIENT))],
)
async def create_appointment(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment_create: AppointmentCreate,
    current_user: User = Depends(get_current_auth_user),
):
    schedule = await validate_appointment(
        session=session,
        appointment_create=appointment_create,
        user=current_user,
    )
    new_appointment = await orm_create_appointment(
        session=session,
        appointment_create=appointment_create,
        patient_id=current_user.id,
        cabinet_id=schedule.cabinet_id,
    )
    return await orm_get_appointment(session=session, appointment_id=new_appointment.id)


@router.get("/me/", response_model=list[AppointmentPatientRead])
async def get_my_appointments(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: User = Depends(require_role(RoleType.PATIENT)),
):
    return await orm_list_appointments(session=session, patient_id=user.id)


@router.get(
    "/{appointment_id}/",
    response_model=AppointmentDoctorRead,
    dependencies=[Depends(require_role(RoleType.ADMIN, RoleType.DOCTOR))],
)
async def get_appointment(
    appointment_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    appointment = await orm_get_appointment(
        session=session, appointment_id=appointment_id
    )
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )
    return appointment


@router.patch(
    "/{appointment_id}/cancel-by-admin",
    response_model=AppointmentAdminRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def cancelled_appointment_by_admin(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment: Appointment = Depends(appointment_by_id),
):
    check_valid_status_for_cancelled(appointment=appointment)

    appointment = await orm_update_appointment_status(
        session=session,
        appointment=appointment,
        appointment_status=AppointmentStatus.CANCELLED,
    )
    return await orm_get_appointment(session=session, appointment_id=appointment.id)


@router.patch(
    "/{appointment_id}/cancel-by-doctor",
    response_model=AppointmentDoctorRead,
)
async def cancelled_appointment_by_doctor(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment: Appointment = Depends(appointment_by_id),
    user: User = Depends(require_role(RoleType.DOCTOR)),
):
    await _ensure_owns_doctor(appointment=appointment, current_user=user)

    check_valid_status_for_cancelled(appointment)

    appointment = await orm_update_appointment_status(
        session=session,
        appointment=appointment,
        appointment_status=AppointmentStatus.CANCELLED,
    )
    return await orm_get_appointment(session=session, appointment_id=appointment.id)


@router.patch(
    "/{appointment_id}/cancel-by-patient", response_model=AppointmentPatientRead
)
async def cancelled_appointment_by_patient(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment: Appointment = Depends(appointment_by_id),
    user: User = Depends(require_role(RoleType.PATIENT)),
):
    await _ensure_owns_patient(appointment=appointment, current_user=user)
    appointment = await orm_update_appointment_status(
        session=session,
        appointment=appointment,
        appointment_status=AppointmentStatus.CANCELLED,
    )
    return await orm_get_appointment(session=session, appointment_id=appointment.id)


@router.patch(
    "/{appointment_id}/confirm",
    response_model=AppointmentAdminRead,
    dependencies=[
        Depends(require_role(RoleType.ADMIN)),
    ],
)
async def confirm_appointment_by_admin(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment: Appointment = Depends(appointment_by_id),
):
    check_valid_status_for_confirmed(appointment)

    appointment = await orm_update_appointment_status(
        session=session,
        appointment=appointment,
        appointment_status=AppointmentStatus.CONFIRMED,
    )
    return await orm_get_appointment(session=session, appointment_id=appointment.id)


@router.patch(
    "/{appointment_id}/completed",
    response_model=AppointmentDoctorRead,
)
async def complete_appointment(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment: Appointment = Depends(appointment_by_id),
    user: User = Depends(require_role(RoleType.DOCTOR, RoleType.ADMIN)),
):
    if user.role.name == RoleType.DOCTOR:
        await _ensure_owns_doctor(appointment=appointment, current_user=user)

    check_valid_status_for_completed(appointment)

    appointment = await orm_update_appointment_status(
        session=session,
        appointment=appointment,
        appointment_status=AppointmentStatus.COMPLETED,
    )
    return await orm_get_appointment(session=session, appointment_id=appointment.id)


@router.patch(
    "/{appointment_id}/no-show",
    response_model=AppointmentDoctorRead,
)
async def set_no_show_appointment(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    appointment: Appointment = Depends(appointment_by_id),
    user: User = Depends(require_role(RoleType.DOCTOR, RoleType.ADMIN)),
):
    if user.role.name == RoleType.DOCTOR:
        await _ensure_owns_doctor(appointment=appointment, current_user=user)

    check_valid_status_for_set_no_show(appointment)

    appointment = await orm_update_appointment_status(
        session=session,
        appointment=appointment,
        appointment_status=AppointmentStatus.NO_SHOW,
    )
    return await orm_get_appointment(session=session, appointment_id=appointment.id)
