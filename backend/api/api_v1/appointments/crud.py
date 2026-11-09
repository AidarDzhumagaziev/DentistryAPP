from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.enums.enums_db import AppointmentStatus

from .schemas import AppointmentBase, AppointmentCreate

from core.models import Appointment


async def orm_get_conflict_between_appointment(
    session: AsyncSession, appointment: AppointmentBase
) -> Appointment | None:
    stmt = select(Appointment).where(
        or_(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.cabinet_id == appointment.cabinet_id,
        ),
        Appointment.starts_at < appointment.ends_at,
        Appointment.ends_at > appointment.starts_at,
        Appointment.status != AppointmentStatus.CANCELLED,
    )
    return await session.scalar(stmt)


async def orm_create_appointment(
    session: AsyncSession, appointment_create: AppointmentCreate
) -> Appointment:
    appointment = Appointment(**appointment_create.model_dump())
    session.add(appointment)
    await session.commit()
    await session.flush()
    return appointment
