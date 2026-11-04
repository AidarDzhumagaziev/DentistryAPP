from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

from api.api_v1.auth.validation import require_role

from .crud import orm_create_specialization
from .schemas import SpecializationRead, SpecializationCreate
from common.enums.enums_db import RoleType
from core.db_helper import db_helper

router = APIRouter(tags=["Specializations"])


@router.post(
    "/",
    response_model=SpecializationRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def create_specialization(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    spec_create: SpecializationCreate,
):
    specialization = await orm_create_specialization(
        session=session, spec_create=spec_create
    )
    return specialization
