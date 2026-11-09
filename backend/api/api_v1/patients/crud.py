from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Patient

from api.api_v1.patients.schemas import PatientCreate


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
