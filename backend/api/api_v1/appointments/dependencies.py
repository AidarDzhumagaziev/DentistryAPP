from typing import Annotated

from fastapi import HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import orm_get_appointment

from core.models import Appointment
from core.db_helper import db_helper


async def appointment_by_id(
    appointment_id: Annotated[int, Path],
    session: Annotated[AsyncSession, db_helper.session_getter],
) -> Appointment:
    appointment = await orm_get_appointment(
        session=session, appointment_id=appointment_id
    )
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )
    return appointment
