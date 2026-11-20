from logging import getLogger
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.crud import orm_create_user
from api.api_v1.auth.utils import hash_password
from api.api_v1.doctors.crud import orm_create_doctor, orm_get_doctor
from api.api_v1.doctors.schemas import DoctorAdminCreate, DoctorRead
from api.api_v1.users.crud import (
    orm_get_user_by_email,
    orm_get_user_by_phone,
)
from common.enums.enums_db import RoleType
from core.db_helper import db_helper
from core.models.users import Role

router = APIRouter(tags=["Admin: doctors"])


logger = getLogger(__name__)


@router.post("/", response_model=DoctorRead, status_code=status.HTTP_201_CREATED)
async def admin_create_doctor(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor_create: DoctorAdminCreate,
):
    if await orm_get_user_by_phone(session=session, phone=doctor_create.user.phone):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Phone already registered"
        )
    if doctor_create.user.email and await orm_get_user_by_email(
        session=session, email=doctor_create.user.email
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    stmt1 = select(Role.id).where(Role.name == RoleType.DOCTOR.value)
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

    user = await orm_create_user(
        session=session,
        user_create=doctor_create.user,
        role_id=role_id,
        password_hash=password_hash,
    )
    doctor = await orm_create_doctor(
        session=session, doctor_create=doctor_create, user_id=user.id
    )

    return await orm_get_doctor(session=session, doctor_id=user.id)
