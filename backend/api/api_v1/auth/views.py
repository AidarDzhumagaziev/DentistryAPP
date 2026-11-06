from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.crud import orm_create_user
from .schemas import TokenInfo
from .validation import get_current_auth_user_for_refresh, validate_auth_user
from api.api_v1.users.schemas import UserCreate, UserRead
from common.enums.enums_db import RoleType
from .utils import (
    create_access_token,
    create_refresh_token,
    hash_password,
)

from core.db_helper import db_helper
from core.models import Role, User

router = APIRouter(tags=["AUTH"])

logger = getLogger(__name__)


@router.post("/register/", response_model=UserRead)
async def registration_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_create: UserCreate,
):
    stmt = select(User).where(User.email == user_create.email)
    result = await session.execute(stmt)
    if result.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    hash_pwd = hash_password(user_create.password)

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

    user = await orm_create_user(
        session=session,
        user_create=user_create,
        role_id=role_id,
        password_hash=hash_pwd,
    )
    return user


@router.post("/login/", response_model=TokenInfo)
async def auth_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await validate_auth_user(
        session=session, email=form_data.username, password=form_data.password
    )
    user_read = UserRead(
        id=user.id, role_id=user.role_id, phone=user.phone, full_name=user.full_name  # type: ignore
    )
    access_token = create_access_token(user_read)
    refresh_token = create_refresh_token(user_read)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/", response_model=TokenInfo)
async def auth_refresh_jwt(user: UserRead = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)
