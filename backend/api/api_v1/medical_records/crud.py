from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MedicalRecord

from .schemas import MedicalRecordCreate


async def orm_get_medical_record_by_appointment_id(
    session: AsyncSession, appointment_id: int
) -> MedicalRecord | None:
    stmt = select(MedicalRecord).where(MedicalRecord.appointment_id == appointment_id)
    return await session.scalar(stmt)


async def orm_create_medical_record(
    session: AsyncSession, medical_record_create: MedicalRecordCreate
) -> MedicalRecord:
    medical_record = MedicalRecord(**medical_record_create.model_dump())
    session.add(medical_record)
    await session.commit()
    await session.flush()
    return medical_record
