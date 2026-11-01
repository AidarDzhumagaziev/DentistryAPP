from typing import Annotated

from fastapi import Depends, Form, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper

from api.api_v1.users.crud import orm_get_user_by_email
from .utils import validate_password


async def validate_auth_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    email: str = Form(),
    password: str = Form(),
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or password"
    )
    if not (user := await orm_get_user_by_email(session, email)):
        raise unauthed_exception
    if not validate_password(password=password, hashed_password=user.password_hash):
        raise unauthed_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user inactive"
        )
    return user
