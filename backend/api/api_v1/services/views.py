from typing import Annotated

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType
from core.db_helper import db_helper

from .schemas import ServiceCreate, ServiceRead
from .crud import orm_create_service

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
    return await orm_create_service(session, service_create)
