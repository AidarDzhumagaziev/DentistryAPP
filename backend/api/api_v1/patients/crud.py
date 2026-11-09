from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Patient

from .schemas import PatientCreate, PatientUpdate


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
    patient_update: PatientUpdate,
    patient: Patient,
    partial: bool = False,
) -> Patient:
    for name, value in patient_update.model_dump(exclude_unset=partial).items():
        setattr(patient, name, value)
    await session.commit()
    await session.flush()
    return patient
