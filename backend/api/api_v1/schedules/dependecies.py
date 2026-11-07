from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import WorkSchedule
from core.db_helper import db_helper

from .schemas import WorkScheduleUpdate, WorkScheduleUpdatePartial
from .validation import validate_time_range, validate_time_to_naive
from .crud import (
    orm_get_conflicting_work_schedule,
    orm_get_work_schedule_by_id,
    orm_update_work_schedule,
)


async def work_schedule_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    work_schedule_id: Annotated[int, Path],
) -> WorkSchedule:
    work_schedule = await orm_get_work_schedule_by_id(
        session=session, work_schedule_id=work_schedule_id
    )
    if work_schedule is not None:
        return work_schedule
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Work schedule not found"
    )


async def get_work_schedule_updating(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    schedule_update: WorkScheduleUpdatePartial | WorkScheduleUpdate,
    schedule: WorkSchedule = Depends(work_schedule_by_id),
) -> WorkSchedule:
    partial = False if isinstance(schedule_update, WorkScheduleUpdate) else True
    new_start = (
        schedule_update.start_time
        if schedule_update.start_time is not None
        else schedule.start_time
    )
    new_end = (
        schedule_update.end_time
        if schedule_update.end_time is not None
        else schedule.end_time
    )
    cabinet_id = (
        schedule_update.cabinet_id
        if schedule_update.cabinet_id is not None
        else schedule.cabinet_id
    )
    validate_time_range(new_start, new_end)
    conflict = await orm_get_conflicting_work_schedule(
        session=session,
        cabinet_id=cabinet_id,
        weekday=schedule.weekday,
        start_time=new_start,
        end_time=new_end,
        exclude_schedule_id=schedule.id,
    )
    if conflict is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The cabinet is occupied during this period",
        )

    return await orm_update_work_schedule(
        session=session,
        schedule=schedule,
        schedule_update=schedule_update,
        partial=partial,
    )
