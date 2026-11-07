from datetime import time
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import WorkScheduleCreate, WorkScheduleUpdate, WorkScheduleUpdatePartial

from core.models import WorkSchedule


async def orm_create_work_schedule(
    session: AsyncSession, work_schedule_create: WorkScheduleCreate
) -> WorkSchedule:
    work_schedule = WorkSchedule(**work_schedule_create.model_dump())
    session.add(work_schedule)
    await session.commit()
    await session.flush()
    return work_schedule


async def orm_get_work_schedules(
    session: AsyncSession, doctor_id: int
) -> Sequence[WorkSchedule]:
    stmt = (
        select(WorkSchedule)
        .where(WorkSchedule.doctor_id == doctor_id)
        .order_by(WorkSchedule.weekday)
    )
    result = await session.scalars(stmt)
    return result.all()


async def orm_get_work_schedule_by_id(
    session: AsyncSession, work_schedule_id: int
) -> WorkSchedule | None:
    stmt = select(WorkSchedule).where(WorkSchedule.id == work_schedule_id)
    return await session.scalar(stmt)


async def orm_update_work_schedule(
    session: AsyncSession,
    schedule: WorkSchedule,
    schedule_update: WorkScheduleUpdate | WorkScheduleUpdatePartial,
    partial: bool = False,
) -> WorkSchedule:
    for name, value in schedule_update.model_dump(exclude_unset=partial).items():
        setattr(schedule, name, value)
    await session.commit()
    await session.flush()
    return schedule


async def orm_get_conflicting_work_schedule(
    session: AsyncSession,
    cabinet_id: int,
    weekday: int,
    start_time: time,
    end_time: time,
    exclude_schedule_id: int,
) -> WorkSchedule | None:
    stmt = (
        select(WorkSchedule)
        .where(
            WorkSchedule.cabinet_id == cabinet_id,
            WorkSchedule.weekday == weekday,
            WorkSchedule.start_time < end_time,
            WorkSchedule.end_time > start_time,
            WorkSchedule.id != exclude_schedule_id,
        )
        .limit(1)
    )
    return await session.scalar(stmt)
