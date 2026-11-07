from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import WorkSchedule
from core.db_helper import db_helper

from .crud import orm_get_work_schedule_by_id


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
