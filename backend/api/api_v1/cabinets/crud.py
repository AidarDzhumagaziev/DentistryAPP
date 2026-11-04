from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CabinetCreate

from core.models import Cabinet


async def orm_create_cabinet(session: AsyncSession, cabinet_in: CabinetCreate):
    cabinet = Cabinet(**cabinet_in.model_dump())
    session.add(cabinet)
    await session.commit()
    await session.flush()
    return cabinet
