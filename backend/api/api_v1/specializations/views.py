from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

from api.api_v1.auth.validation import require_role

from .crud import (
    orm_create_specialization,
    orm_delete_specialization,
    orm_get_specializations,
    orm_update_specialization,
)
from .schemas import SpecializationRead, SpecializationCreate, SpecializationUpdate
from .dependecies import specialization_by_id
from common.enums.enums_db import RoleType
from core.db_helper import db_helper
from core.models import Specialization

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


@router.get(
    "/", response_model=list[SpecializationRead], status_code=status.HTTP_200_OK
)
async def get_specializations(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await orm_get_specializations(session)


@router.get("/{specialization_id}/", response_model=SpecializationRead)
async def get_specialization(
    specialization: Specialization = Depends(specialization_by_id),
):
    return specialization


@router.put("/{specialization_id}/")
async def update_specialization(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    specialization_update: SpecializationUpdate,
    specialization: Specialization = Depends(specialization_by_id),
):
    return await orm_update_specialization(
        session=session,
        specialization=specialization,
        specialization_update=specialization_update,
    )


@router.delete("/{specialization_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specialization(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    specialization: Specialization = Depends(specialization_by_id),
):
    await orm_delete_specialization(session=session, specialization=specialization)
