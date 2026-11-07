from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import require_role
from api.api_v1.schedules.validation import validate_time_to_naive
from common.enums.enums_db import RoleType

from core.db_helper import db_helper
from core.models import WorkSchedule

from .crud import (
    orm_create_work_schedule,
    orm_get_conflicting_work_schedule,
    orm_get_work_schedules,
    orm_update_work_schedule,
)
from .schemas import (
    WorkScheduleRead,
    WorkScheduleCreate,
    WorkScheduleUpdate,
    WorkScheduleUpdatePartial,
)
from .dependecies import get_work_schedule_updating, work_schedule_by_id

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


@router.get("/{doctor_id}/", response_model=list[WorkScheduleRead])
async def get_all_the_work_schedules(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    doctor_id: Annotated[int, Path],
):
    return await orm_get_work_schedules(session=session, doctor_id=doctor_id)


@router.get("/{work_schedule_id}/", response_model=WorkScheduleRead)
async def get_work_schedule(work_schedule: WorkSchedule = Depends(work_schedule_by_id)):
    return work_schedule


@router.put(
    "/{work_schedule_id}/",
    response_model=WorkScheduleRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_work_schedule(
    schedule: WorkSchedule = Depends(get_work_schedule_updating),
):
    return schedule


@router.patch(
    "/{work_schedule_id}/",
    response_model=WorkScheduleRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_partial_work_schedule(
    schedule: WorkSchedule = Depends(get_work_schedule_updating),
):
    return schedule
