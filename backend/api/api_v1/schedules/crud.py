from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import WorkScheduleCreate

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
