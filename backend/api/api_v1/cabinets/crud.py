from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CabinetCreate

from core.models import Cabinet


async def orm_create_cabinet(session: AsyncSession, cabinet_in: CabinetCreate):
    cabinet = Cabinet(**cabinet_in.model_dump())
    session.add(cabinet)
    await session.commit()
    await session.flush()
    return cabinet


async def orm_get_cabinets(session: AsyncSession):
    stmt = select(Cabinet).order_by(Cabinet.number)
    result = await session.scalars(stmt)
    return result.all()


async def orm_get_cabinet(session: AsyncSession, cabinet_id: int):
    stmt = select(Cabinet).where(Cabinet.id == cabinet_id)
    return await session.scalar(stmt)
