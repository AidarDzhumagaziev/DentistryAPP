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
