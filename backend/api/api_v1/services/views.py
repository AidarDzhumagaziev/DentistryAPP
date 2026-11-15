from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType
from core.db_helper import db_helper
from core.models import Service

from .schemas import ServiceCreate, ServiceRead, ServiceUpdate, ServiceUpdatePartial
from .crud import (
    orm_create_service,
    orm_delete_service,
    orm_get_service_by_name,
    orm_get_services,
    orm_update_service,
)
from .dependencies import service_by_id

router = APIRouter(tags=["Services"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def create_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service_create: ServiceCreate,
):
    exists = await orm_get_service_by_name(session, service_create.name)
    if exists is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Service {service_create.name} already exists",
        )
    return await orm_create_service(session, service_create)


@router.get("/", response_model=list[ServiceRead])
async def get_services(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await orm_get_services(session=session)


@router.get("/{service_id}/", response_model=ServiceRead)
async def get_service(
    service: Service = Depends(service_by_id),
):
    return service


@router.put(
    "/{service_id}/",
    response_model=ServiceRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service_update: ServiceUpdate,
    service: Service = Depends(service_by_id),
):
    return await orm_update_service(
        session=session, service_update=service_update, service=service
    )


@router.patch(
    "/{service_id}/",
    response_model=ServiceRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_service_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service_update: ServiceUpdatePartial,
    service: Service = Depends(service_by_id),
):
    return await orm_update_service(
        session=session, service_update=service_update, service=service, partial=True
    )


@router.delete(
    "/{service_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def delete_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service: Service = Depends(service_by_id),
):
    service.is_active = False
    await session.commit()
