from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CabinetCreate, CabinetUpdate, CabinetUpdatePartial

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


async def orm_update_cabinet(
    session: AsyncSession,
    cabinet_update: CabinetUpdate | CabinetUpdatePartial,
    cabinet: Cabinet,
    partial: bool = False,
):
    for name, value in cabinet_update.model_dump(exclude_unset=partial).items():
        setattr(cabinet, name, value)
    await session.commit()
    return cabinet


async def orm_delete_cabinet(session: AsyncSession, cabinet: Cabinet):
    await session.delete(cabinet)
    await session.commit()
