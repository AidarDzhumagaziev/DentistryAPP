from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Doctor, User, DoctorSpecialization

from .schemas import DoctorCreate


async def orm_create_doctor(session: AsyncSession, doctor_create: DoctorCreate):
    doctor = Doctor(
        user_id=doctor_create.user_id,
        bio=doctor_create.bio,
        experience_years=doctor_create.experience_years,
        photo_url=doctor_create.photo_url,
        is_active=doctor_create.is_active,
    )
    doctor_specializations = [
        DoctorSpecialization(doctor_id=doctor_create.user_id, specialization_id=s_id)
        for s_id in doctor_create.specializations_ids
    ]
    session.add(doctor)
    session.add_all(doctor_specializations)
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


async def orm_get_doctors(session: AsyncSession) -> Sequence[Doctor]:
    stmt = (
        select(Doctor)
        .join(User, User.id == Doctor.user_id)
        .options(
            selectinload(Doctor.user),
            selectinload(Doctor.specializations).selectinload(
                DoctorSpecialization.specialization
            ),
        )
        .order_by(User.full_name)
    )
    result = await session.scalars(stmt)
    return result.all()
