from typing import Annotated

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType

from .schemas import CabinetRead, CabinetCreate
from .crud import orm_create_cabinet, orm_get_cabinets

router = APIRouter(tags=["Cabinets"])


@router.post(
    "/",
    response_model=CabinetRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def create_cabinet(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    cabinet_create: CabinetCreate,
):
    return await orm_create_cabinet(session=session, cabinet_in=cabinet_create)


@router.get("/", response_model=list[CabinetRead])
async def get_cabinets(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await orm_get_cabinets(session)
