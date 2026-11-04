from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Specialization
from .schemas import SpecializationCreate


async def orm_create_specialization(
    session: AsyncSession, spec_create: SpecializationCreate
):
    obj = Specialization(**spec_create.model_dump())
    session.add(obj)
    await session.flush()
    await session.commit()
    return obj


async def orm_get_specializations(session: AsyncSession):
    stmt = select(Specialization).order_by(Specialization.name)
    result = await session.scalars(stmt)
    return result.all()


async def orm_get_specialization(session: AsyncSession, specialization_id: int):
    stmt = select(Specialization).where(Specialization.id == specialization_id)
    return await session.scalar(stmt)
