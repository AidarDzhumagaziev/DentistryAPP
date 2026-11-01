from logging import getLogger
from typing import Annotated

from fastapi import Depends, Form, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper

from api.api_v1.users.crud import orm_get_user_by_email, orm_get_user_by_id
from .utils import (
    validate_password,
    decode_jwt,
    TOKEN_TYPE_FIELD,
    REFRESH_TOKEN_TYPE,
    ACCESS_TOKEN_TYPE,
)

logger = getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


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


def validate_token_type(payload: dict, token_type: str):
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    logger.warning(
        f"invalid token type: excepted {token_type}, got {current_token_type}"
    )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token",
    )


def get_current_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        logger.error(f"invalid token error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    return payload


async def get_current_auth_user_for_refresh(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    payload: dict = Depends(get_current_token_payload),
):
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    user_id: int = payload.get("sub")  # type: ignore
    if user := await orm_get_user_by_id(session=session, user_id=user_id):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
    )
