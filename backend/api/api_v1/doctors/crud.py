from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Doctor

from .schemas import DoctorCreate


async def orm_create_doctor(session: AsyncSession, doctor_create: DoctorCreate):
    doctor = Doctor(**doctor_create.model_dump())
    session.add(doctor)
    await session.commit()
    await session.flush()
    return doctor


async def orm_get_doctor_by_user_id(session: AsyncSession, user_id: int):
    stmt = (
        select(Doctor)
        .options(selectinload(Doctor.user))
        .where(Doctor.user_id == user_id)
    )
    return await session.scalar(stmt)
