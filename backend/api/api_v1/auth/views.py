from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from .dependecies import create_user
from .schemas import TokenInfo
from .validation import get_current_auth_user_for_refresh, validate_auth_user
from api.api_v1.users.schemas import UserRead
from .utils import (
    create_access_token,
    create_refresh_token,
)

from core.db_helper import db_helper
from core.models import User

router = APIRouter(tags=["AUTH"])

logger = getLogger(__name__)


@router.post("/register/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def registration_user(
    user: User = Depends(create_user),
):
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
        id=user.id,
        role_id=user.role_id,
        phone=user.phone,
        full_name=user.full_name,
        email=user.email,
    )
    access_token = create_access_token(user_read)
    refresh_token = create_refresh_token(user_read)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/", response_model=TokenInfo)
async def auth_refresh_jwt(user: UserRead = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)
