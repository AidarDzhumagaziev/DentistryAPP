from typing import Annotated, Sequence

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import orm_get_doctor, orm_get_doctors

from core.db_helper import db_helper
from core.models import Doctor


async def get_all_doctors(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Sequence[Doctor]:
    doctors = await orm_get_doctors(session=session, is_active=True)
    return doctors


async def doctor_by_id(
    doctor_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Doctor:
    doctor = await orm_get_doctor(session=session, doctor_id=doctor_id, is_active=True)
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )
    return doctor
