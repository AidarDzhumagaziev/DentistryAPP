from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import DoctorRead
from .crud import orm_get_doctor, orm_get_doctors
from .validation import validation_doctor

from core.db_helper import db_helper


async def get_all_doctors(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[DoctorRead]:
    doctors = await orm_get_doctors(session=session)
    doctors_read = [validation_doctor(doctor) for doctor in doctors]
    return doctors_read


async def doctor_by_id(
    doctor_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> DoctorRead:
    doctor = await orm_get_doctor(session=session, doctor_id=doctor_id)
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )
    doctor_read = validation_doctor(doctor)
    return doctor_read
