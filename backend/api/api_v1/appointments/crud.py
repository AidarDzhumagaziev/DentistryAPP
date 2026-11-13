from typing import Sequence

from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from common.enums.enums_db import AppointmentStatus

from .schemas import AppointmentBase, AppointmentCreate

from core.models import Appointment, Doctor, DoctorSpecialization


async def orm_get_conflict_between_appointment(
    session: AsyncSession, appointment: AppointmentCreate
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
    session: AsyncSession, appointment_create: AppointmentCreate, patient_id: int
) -> Appointment:
    appointment = Appointment(
        doctor_id=appointment_create.doctor_id,
        patient_id=patient_id,
        service_id=appointment_create.service_id,
        cabinet_id=appointment_create.cabinet_id,
        starts_at=appointment_create.starts_at,
        ends_at=appointment_create.ends_at,
    )
    session.add(appointment)
    await session.commit()
    await session.flush()
    return appointment


async def orm_get_appointment(
    session: AsyncSession, appointment_id: int
) -> Appointment | None:
    stmt = (
        select(Appointment)
        .options(
            selectinload(Appointment.patient),
            selectinload(Appointment.doctor)
            .selectinload(Doctor.specializations)
            .selectinload(DoctorSpecialization.specialization),
            selectinload(Appointment.service),
            selectinload(Appointment.cabinet),
        )
        .where(Appointment.id == appointment_id)
    )
    return await session.scalar(stmt)


async def orm_get_appointment_by_doctor_id(
    session: AsyncSession, doctor_id: int
) -> Sequence[Appointment]:
    stmt = (
        select(Appointment)
        .options(
            selectinload(Appointment.patient),
            selectinload(Appointment.doctor),
            selectinload(Appointment.service),
            selectinload(Appointment.cabinet),
        )
        .where(Appointment.doctor_id == doctor_id)
    )
    result = await session.scalars(stmt)
    return result.all()


async def orm_update_appointment_status(
    session: AsyncSession,
    appointment: Appointment,
    appointment_status: AppointmentStatus,
) -> Appointment:
    appointment.status = appointment_status
    await session.commit()
    return appointment
