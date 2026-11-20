from datetime import datetime
from typing import Sequence

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from common.enums.enums_db import AppointmentStatus

from .schemas import AppointmentCreate

from core.models import Appointment, Doctor, DoctorSpecialization, Patient


async def orm_get_conflict_between_appointment(
    session: AsyncSession, appointment: AppointmentCreate
) -> Appointment | None:
    stmt = select(Appointment).where(
        or_(Appointment.doctor_id == appointment.doctor_id),
        Appointment.starts_at < appointment.ends_at,
        Appointment.ends_at > appointment.starts_at,
        Appointment.status != AppointmentStatus.CANCELLED,
    )
    return await session.scalar(stmt)


async def orm_create_appointment(
    session: AsyncSession,
    appointment_create: AppointmentCreate,
    patient_id: int,
    cabinet_id: int,
) -> Appointment:
    appointment = Appointment(
        doctor_id=appointment_create.doctor_id,
        patient_id=patient_id,
        service_id=appointment_create.service_id,
        cabinet_id=cabinet_id,
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
            selectinload(Appointment.patient).selectinload(Patient.user),
            selectinload(Appointment.doctor).selectinload(Doctor.user),
            selectinload(Appointment.doctor)
            .selectinload(Doctor.specializations)
            .selectinload(DoctorSpecialization.specialization),
            selectinload(Appointment.service),
            selectinload(Appointment.cabinet),
            joinedload(Appointment.medical_record),
        )
        .where(Appointment.id == appointment_id)
    )
    return await session.scalar(stmt)


async def orm_get_appointments_by_doctor_id(
    session: AsyncSession, doctor_id: int
) -> Sequence[Appointment]:
    stmt = (
        select(Appointment)
        .options(
            selectinload(Appointment.patient).selectinload(Patient.user),
            selectinload(Appointment.doctor).selectinload(Doctor.specializations),
            selectinload(Appointment.service),
            selectinload(Appointment.cabinet),
        )
        .where(Appointment.doctor_id == doctor_id)
    )
    result = await session.scalars(stmt)
    return result.all()


async def orm_get_appointments_by_patient_id_and_datetime(
    session: AsyncSession, patient_id: int, start: datetime, end: datetime
):
    stmt = select(Appointment).where(
        Appointment.patient_id == patient_id,
        Appointment.starts_at < end,
        Appointment.ends_at > start,
    )
    return await session.scalar(stmt)


async def orm_update_appointment_status(
    session: AsyncSession,
    appointment: Appointment,
    appointment_status: AppointmentStatus,
) -> Appointment:
    appointment.status = appointment_status
    await session.commit()
    return appointment


async def orm_list_appointments(
    session: AsyncSession,
    patient_id: int | None = None,
    doctor_id: int | None = None,
    status: AppointmentStatus | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = 50,
    offset: int = 0,
) -> Sequence[Appointment]:
    stmt = select(Appointment).options(
        selectinload(Appointment.patient).selectinload(Patient.user),
        selectinload(Appointment.doctor).selectinload(Doctor.user),
        selectinload(Appointment.doctor)
        .selectinload(Doctor.specializations)
        .selectinload(DoctorSpecialization.specialization),
        selectinload(Appointment.service),
        selectinload(Appointment.cabinet),
        joinedload(Appointment.medical_record),
    )
    if patient_id is not None:
        stmt = stmt.where(Appointment.patient_id == patient_id)
    if doctor_id is not None:
        stmt = stmt.where(Appointment.doctor_id == doctor_id)
    if status is not None:
        stmt = stmt.where(Appointment.status == status)
    if date_from is not None:
        stmt = stmt.where(Appointment.starts_at >= date_from)
    if date_to is not None:
        stmt = stmt.where(Appointment.ends_at <= date_to)

    stmt = stmt.order_by(Appointment.starts_at.desc()).limit(limit).offset(offset)

    result = await session.scalars(stmt)
    return result.all()


async def orm_get_booked_appointment_in_diaposon(
    session: AsyncSession, doctor_id: int, start_min: datetime, end_max: datetime
) -> Sequence[Appointment]:
    stmt = select(Appointment).where(
        Appointment.doctor_id == doctor_id,
        Appointment.status.in_(
            [AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED]
        ),
        Appointment.starts_at < end_max,
        Appointment.ends_at > start_min,
    )
    result = await session.scalars(stmt)
    return result.all()


async def orm_has_prior_consultation(
    session: AsyncSession,
    patient_id: int,
    consultation_service_id: int,
    before: datetime,
) -> int | None:
    stmt = select(Appointment.id).where(
        Appointment.patient_id == patient_id,
        Appointment.service_id == consultation_service_id,
        Appointment.starts_at < before,
    )
    return await session.scalar(stmt)
