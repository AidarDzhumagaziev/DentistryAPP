from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType

from core.db_helper import db_helper
from core.models import WorkSchedule

from .validation import validate_time_range
from .crud import (
    orm_create_work_schedule,
    orm_get_work_schedules,
)
from .schemas import (
    WorkScheduleRead,
    WorkScheduleCreate,
)
from .dependecies import (
    get_conflicting_work_schedule,
    get_work_schedule_updating,
    work_schedule_by_id,
)

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
    validate_time_range(work_schedule_create.start_time, work_schedule_create.end_time)
    conflict = await get_conflicting_work_schedule(
        session=session,
        weekday=work_schedule_create.weekday,
        start_time=work_schedule_create.start_time,
        cabinet_id=work_schedule_create.cabinet_id,
        end_time=work_schedule_create.end_time,
    )
    if conflict is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The cabinet is occupied during this period",
        )
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
