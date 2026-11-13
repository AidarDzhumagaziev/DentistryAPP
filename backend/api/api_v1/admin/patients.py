from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.patients.crud import orm_search_patients
from api.api_v1.users.schemas import UserRead
from core.db_helper import db_helper

router = APIRouter(tags=["Admin: Patients"])


@router.get("/", response_model=list[UserRead])
async def admin_search_patients(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    phone: str | None = None,
    full_name: str | None = None,
):
    return await orm_search_patients(session=session, phone=phone, full_name=full_name)
