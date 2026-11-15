from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.enums.enums_db import RoleType
from core.models import Patient, User, Role

from .schemas import PatientCreate, PatientUpdate, PatientUpdatePartial


async def orm_create_patient(
    session: AsyncSession, patient_create: PatientCreate
) -> Patient:
    patient = Patient(**patient_create.model_dump())
    session.add(patient)
    await session.commit()
    await session.flush()
    return patient


async def orm_get_patient(session: AsyncSession, user_id: int) -> Patient | None:
    stmt = select(Patient).where(Patient.user_id == user_id)
    return await session.scalar(stmt)


async def orm_get_patients(session: AsyncSession) -> Sequence[Patient]:
    stmt = select(Patient).order_by(Patient.user_id)
    result = await session.scalars(stmt)
    return result.all()


async def orm_update_patient(
    session: AsyncSession,
    patient_update: PatientUpdate | PatientUpdatePartial,
    patient: Patient,
    partial: bool = False,
) -> Patient:
    for name, value in patient_update.model_dump(exclude_unset=partial).items():
        setattr(patient, name, value)
    await session.commit()
    await session.flush()
    return patient


async def orm_delete_patient(session: AsyncSession, patient: Patient) -> None:
    await session.delete(patient)
    await session.commit()


async def orm_search_patients(
    session: AsyncSession,
    phone: str | None = None,
    full_name: str | None = None,
    limit: int = 50,
    offset: int = 0,
):
    stmt = (
        select(User)
        .join(Role, Role.id == User.role_id)
        .where(Role.name == RoleType.ADMIN)
    )
    if phone:
        normalized = (
            phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        )
        stmt = stmt.where(User.phone.ilike(f"%{normalized}%"))
    if full_name:
        stmt = stmt.where(User.full_name.ilike(f"%{full_name}%"))
    stmt = stmt.order_by(User.full_name).limit(limit).offset(offset)
    result = await session.scalars(stmt)
    return result.all()
