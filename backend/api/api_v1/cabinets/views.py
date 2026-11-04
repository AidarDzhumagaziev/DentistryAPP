from typing import Annotated

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Cabinet

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType

from .dependecies import cabinet_by_id
from .schemas import CabinetRead, CabinetCreate, CabinetUpdate, CabinetUpdatePartial
from .crud import (
    orm_create_cabinet,
    orm_delete_cabinet,
    orm_get_cabinets,
    orm_update_cabinet,
)

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


@router.get("/{cabinet_id}/", response_model=CabinetRead)
async def get_cabinet(cabinet: Cabinet = Depends(cabinet_by_id)):
    return cabinet


@router.put(
    "/{cabinet_id}/",
    response_model=CabinetRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_cabinet(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    cabinet_update: CabinetUpdate,
    cabinet: Cabinet = Depends(cabinet_by_id),
):
    return await orm_update_cabinet(
        session=session, cabinet_update=cabinet_update, cabinet=cabinet
    )


@router.patch("/{cabinet_id}/")
async def update_partial_cabinet(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    cabinet_update: CabinetUpdatePartial,
    cabinet: Cabinet = Depends(cabinet_by_id),
):
    return await orm_update_cabinet(
        session=session, cabinet_update=cabinet_update, cabinet=cabinet, partial=True
    )


@router.delete(
    "/{cabinet_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def delete_cabinet(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    cabinet: Cabinet = Depends(cabinet_by_id),
):
    await orm_delete_cabinet(session=session, cabinet=cabinet)
