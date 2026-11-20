from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import get_current_auth_user
from core.db_helper import db_helper
from core.models.users import User

from .crud import orm_get_user_by_id, orm_get_users
from .schemas import UserRead, UserProfileRead

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[UserRead])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await orm_get_users(session)


@router.get("/me/", response_model=UserProfileRead)
async def get_profile(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_auth_user),
):
    return await orm_get_user_by_id(session=session, user_id=current_user.id)
