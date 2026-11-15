from logging import getLogger
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.users.crud import orm_get_user_by_id

from .crud import orm_create_user
from .utils import hash_password
from api.api_v1.users.schemas import UserCreate
from common.enums.enums_db import RoleType
from core.db_helper import db_helper
from core.models import User, Role

logger = getLogger(__name__)


async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_create: UserCreate,
) -> User:
    stmt = select(User).where((User.email == user_create.email))
    result = await session.execute(stmt)
    if result.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    stmt_0 = select(User).where(User.phone == user_create.phone)
    result = await session.execute(stmt_0)
    if result.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Phone already registered"
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

    hash_pwd = hash_password(user_create.password)
    user = await orm_create_user(
        session=session,
        user_create=user_create,
        role_id=role_id,
        password_hash=hash_pwd,
    )
    return await orm_get_user_by_id(session=session, user_id=user.id)  # type: ignore
