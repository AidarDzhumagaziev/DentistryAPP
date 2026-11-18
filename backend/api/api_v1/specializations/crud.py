from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Specialization
from .schemas import SpecializationCreate, SpecializationUpdate


async def orm_create_specialization(
    session: AsyncSession, spec_create: SpecializationCreate
) -> Specialization:
    obj = Specialization(**spec_create.model_dump())
    session.add(obj)
    await session.flush()
    await session.commit()
    return obj


async def orm_get_specializations(session: AsyncSession) -> Sequence[Specialization]:
    stmt = select(Specialization).order_by(Specialization.name)
    result = await session.scalars(stmt)
    return result.all()


async def orm_get_specialization(
    session: AsyncSession, specialization_id: int
) -> Specialization | None:
    stmt = select(Specialization).where(Specialization.id == specialization_id)
    return await session.scalar(stmt)


async def orm_get_specialization_by_name(session: AsyncSession, name: str):
    stmt = select(Specialization).where(Specialization.name == name)
    return await session.scalar(stmt)


async def orm_update_specialization(
    session: AsyncSession,
    specialization: Specialization,
    specialization_update: SpecializationUpdate,
) -> Specialization:
    for name, value in specialization_update.model_dump().items():
        setattr(specialization, name, value)
    await session.commit()
    return specialization


async def orm_delete_specialization(
    session: AsyncSession, specialization: Specialization
) -> None:
    await session.delete(specialization)
    await session.commit()
