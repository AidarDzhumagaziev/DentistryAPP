from typing import Annotated

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType

from core.db_helper import db_helper

from .crud import orm_create_work_schedule
from .schemas import WorkScheduleRead, WorkScheduleCreate

router = APIRouter(tags=["Schedules"])


@router.post(
    "/",
    response_model=WorkScheduleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def create_work_schedule(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    work_schedule_create: WorkScheduleCreate,
):
    return await orm_create_work_schedule(
        session=session, work_schedule_create=work_schedule_create
    )
