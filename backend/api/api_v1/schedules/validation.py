from datetime import time

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import (
    orm_get_conflicting_work_schedule_by_cabinet,
    orm_get_conflicting_work_schedule_by_time,
)


def validate_time_to_naive(t: time):
    return t.replace(tzinfo=None) if t.tzinfo else t


def validate_time_range(start_time: time, end_time: time):
    if validate_time_to_naive(start_time) >= validate_time_to_naive(end_time):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Start time must be before end time",
        )


async def validate_schedule_no_conflict(
    session: AsyncSession,
    doctor_id: int,
    cabinet_id: int,
    weekday: int,
    start_time: time,
    end_time: time,
    exclude_schedule_id: int | None = None,
):
    conflict_cabinet = await orm_get_conflicting_work_schedule_by_cabinet(
        session=session,
        cabinet_id=cabinet_id,
        weekday=weekday,
        start_time=start_time,
        end_time=end_time,
        exclude_schedule_id=exclude_schedule_id,
    )
    if conflict_cabinet is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The cabinet is occupied during this period",
        )
    conflict_time = await orm_get_conflicting_work_schedule_by_time(
        session=session,
        doctor_id=doctor_id,
        weekday=weekday,
        start_time=start_time,
        end_time=end_time,
        exclude_schedule_id=exclude_schedule_id,
    )
    if conflict_time is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The doctor has already set a work schedule at this time.",
        )
