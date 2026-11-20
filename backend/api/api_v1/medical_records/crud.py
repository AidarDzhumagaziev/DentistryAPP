from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MedicalRecord

from .schemas import MedicalRecordCreate, MedicalRecordUpdatePartial


async def orm_get_medical_record_by_appointment_id(
    session: AsyncSession, appointment_id: int
) -> MedicalRecord | None:
    stmt = select(MedicalRecord).where(MedicalRecord.appointment_id == appointment_id)
    return await session.scalar(stmt)


async def orm_create_medical_record(
    session: AsyncSession,
    medical_record_create: MedicalRecordCreate,
    appointment_id: int,
) -> MedicalRecord:
    medical_record = MedicalRecord(
        appointment_id=appointment_id,
        complaints=medical_record_create.complaints,
        objective_findings=medical_record_create.objective_findings,
        diagnosis=medical_record_create.diagnosis,
        treatment_plan=medical_record_create.treatment_plan,
    )
    session.add(medical_record)
    await session.commit()
    await session.flush()
    return medical_record


async def orm_update_medical_record(
    session: AsyncSession,
    medical_record: MedicalRecord,
    medical_record_update: MedicalRecordUpdatePartial,
) -> MedicalRecord:
    for name, value in medical_record_update.model_dump(exclude_unset=True).items():
        setattr(medical_record, name, value)
    await session.commit()
    return medical_record
