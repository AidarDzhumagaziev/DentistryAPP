from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.specializations.schemas import SpecializationRead
from api.api_v1.users.schemas import UserRead

from .schemas import DoctorRead
from .crud import orm_get_doctor, orm_get_doctors

from core.db_helper import db_helper
from core.models import Doctor


async def get_all_doctors(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[DoctorRead]:
    doctors = await orm_get_doctors(session=session)
    doctors_read = [
        DoctorRead(
            user_id=doctor.user_id,
            experience_years=doctor.experience_years,
            bio=doctor.bio,
            photo_url=doctor.photo_url,
            is_active=doctor.is_active,
            user=UserRead(
                phone=doctor.user.phone,
                full_name=doctor.user.full_name,
                id=doctor.user.id,
                role_id=doctor.user.role_id,
            ),
            specializations=[
                SpecializationRead(
                    id=spec.specialization.id, name=spec.specialization.name
                )
                for spec in doctor.specializations
            ],
        )
        for doctor in doctors
    ]
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
    doctor_read = DoctorRead(
        user_id=doctor.user_id,
        experience_years=doctor.experience_years,
        bio=doctor.bio,
        photo_url=doctor.photo_url,
        is_active=doctor.is_active,
        user=UserRead(
            phone=doctor.user.phone,
            full_name=doctor.user.full_name,
            id=doctor.user.id,
            role_id=doctor.user.role_id,
        ),
        specializations=[
            SpecializationRead(id=spec.specialization.id, name=spec.specialization.name)
            for spec in doctor.specializations
        ],
    )
    return doctor_read
