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
