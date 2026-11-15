from logging import getLogger
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.crud import orm_create_user
from api.api_v1.auth.utils import hash_password
from api.api_v1.patients.crud import orm_search_patients
from api.api_v1.users.crud import (
    orm_get_user_by_email,
    orm_get_user_by_id,
    orm_get_user_by_phone,
)
from api.api_v1.users.schemas import UserAdminCreate, UserRead
from common.enums.enums_db import RoleType
from core.db_helper import db_helper
from core.models.users import Role

router = APIRouter(tags=["Admin: Patients"])


logger = getLogger(__name__)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def admin_create_patient(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    patient_create: UserAdminCreate,
):
    if await orm_get_user_by_phone(session=session, phone=patient_create.phone):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Phone already registered"
        )
    if patient_create.email and await orm_get_user_by_email(
        session=session, email=patient_create.email
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    stmt1 = select(Role.id).where(Role.name == RoleType.PATIENT.value)
    role_id = await session.scalar(stmt1)
    if role_id is None:
        logger.error(
            f"Role {RoleType.PATIENT.value!r} is not initialized in the database"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Role {RoleType.PATIENT.value!r} is not found",
        )

    temp_password = secrets.token_urlsafe(12)
    password_hash = hash_password(temp_password)

    patient = await orm_create_user(
        session=session,
        user_create=patient_create,
        role_id=role_id,
        password_hash=password_hash,
    )
    return await orm_get_user_by_id(session=session, user_id=patient.id)


@router.get("/", response_model=list[UserRead])
async def admin_search_patients(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    phone: str | None = None,
    full_name: str | None = None,
):
    return await orm_search_patients(session=session, phone=phone, full_name=full_name)
