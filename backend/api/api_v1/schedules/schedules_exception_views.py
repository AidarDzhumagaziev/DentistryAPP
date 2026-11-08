from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType

from core.db_helper import db_helper
from core.models import ScheduleException

from .schemas import (
    ScheduleExceptionRead,
    ScheduleExceptionCreate,
)
from .crud import (
    orm_create_schedule_exception,
    orm_delete_schedule_exception,
    orm_get_schedule_exception_by_date,
)
from .dependecies import schedule_exception_by_id, validation_schedule_exception

router = APIRouter(tags=["Schedule Exception"])


@router.post(
    "/",
    response_model=ScheduleExceptionRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def create_schedule_exception(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    schedule_create: ScheduleExceptionCreate,
):
    schedule = await orm_get_schedule_exception_by_date(
        session=session,
        doctor_id=schedule_create.doctor_id,
        date_to=schedule_create.date_to,
        date_from=schedule_create.date_from,
        exclude_schedule_id=None,
    )
    if schedule is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Doctor already has an exception from the schedule",
        )
    return await orm_create_schedule_exception(
        session=session, schedule_create=schedule_create
    )


@router.get("/{schedule_exception_id}/", response_model=ScheduleExceptionRead)
async def get_schedule_exception(
    schedule: ScheduleException = Depends(schedule_exception_by_id),
):
    return schedule


@router.put(
    "/{schedule_exception_id}/",
    response_model=ScheduleExceptionRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_schedule_exception(
    schedule: ScheduleException = Depends(validation_schedule_exception),
):
    return schedule


@router.patch(
    "/{schedule_exception_id}/",
    response_model=ScheduleExceptionRead,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def update_schedule_exception_partial(
    schedule: ScheduleException = Depends(validation_schedule_exception),
):
    return schedule


@router.delete(
    "/{schedule_exception_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)
async def delete_schedule_exception(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    schedule: ScheduleException = Depends(schedule_exception_by_id),
):
    await orm_delete_schedule_exception(session=session, schedule=schedule)
