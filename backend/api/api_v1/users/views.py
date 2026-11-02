from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper

from .crud import orm_get_users
from .schemas import UserRead

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[UserRead])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await orm_get_users(session)
