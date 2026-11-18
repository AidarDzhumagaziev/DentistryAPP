from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType

from core.db_helper import db_helper
from core.models import Patient, User

from .dependecies import patient_by_id
from .crud import (
    orm_create_patient,
    orm_delete_patient,
    orm_get_patient,
    orm_get_patients,
    orm_update_patient,
)
from .schemas import (
    PatientAdminCreate,
    PatientOwnUpdatePartial,
    PatientRead,
    PatientUpdate,
    PatientUpdatePartial,
    PatientCreate,
)

router = APIRouter(tags=["Patients"])


@router.post(
    "/",
    response_model=PatientRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def create_patient(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    patient_create: PatientAdminCreate,
):
    patient = await orm_get_patient(session=session, user_id=patient_create.user_id)
    if patient is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has patient profile",
        )
    return await orm_create_patient(
        session=session,
        user_id=patient_create.user_id,
        birth_date=patient_create.birth_date,
        allergies=patient_create.allergies,
        chronic_diseas=patient_create.chronic_diseas,
    )


@router.get(
    "/",
    response_model=list[PatientRead],
    dependencies=[Depends(require_role(RoleType.ADMIN, RoleType.DOCTOR))],
)
async def get_patients(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await orm_get_patients(session=session)


@router.get("/me/", response_model=PatientRead)
async def get_patient_profile(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: User = Depends(require_role(RoleType.PATIENT)),
):
    patient = await orm_get_patient(session=session, user_id=user.id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return patient


@router.get(
    "/{patient_id}/",
    response_model=PatientRead,
    dependencies=[Depends(require_role(RoleType.ADMIN, RoleType.DOCTOR))],
)
async def get_patient(patient: Patient = Depends(patient_by_id)):
    return patient


@router.put(
    "/{patient_id}/",
    response_model=PatientRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_patient(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    patient_update: PatientUpdate,
    patient: Patient = Depends(patient_by_id),
):
    return await orm_update_patient(
        session=session, patient=patient, patient_update=patient_update
    )


@router.patch("/me/", response_model=PatientRead)
async def update_own_profile(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    patient_update: PatientOwnUpdatePartial,
    user: User = Depends(require_role(RoleType.PATIENT)),
):
    patient = await orm_get_patient(session=session, user_id=user.id)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has patient profile",
        )
    return await orm_update_patient(
        session=session, patient=patient, patient_update=patient_update, partial=True
    )


@router.patch(
    "/{patient_id}/",
    response_model=PatientRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_patient_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    patient_update: PatientUpdatePartial,
    patient: Patient = Depends(patient_by_id),
):
    return await orm_update_patient(
        session=session, patient=patient, patient_update=patient_update, partial=True
    )


@router.delete(
    "/{patient_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def delete_patient(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    patient: Patient = Depends(patient_by_id),
):
    await orm_delete_patient(session=session, patient=patient)


@router.post("/me/", status_code=status.HTTP_201_CREATED, response_model=PatientRead)
async def create_profile_by_patient(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    patient_create: PatientCreate,
    user: User = Depends(require_role(RoleType.PATIENT)),
):
    patient = await orm_get_patient(session=session, user_id=user.id)
    if patient is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has patient profile",
        )
    patient = await orm_create_patient(
        session=session,
        user_id=user.id,
        birth_date=patient_create.birth_date,
        allergies=patient_create.allergies,
        chronic_diseas=patient_create.chronic_diseas,
    )
    return await orm_get_patient(session=session, user_id=patient.user_id)
