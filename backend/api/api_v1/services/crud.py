from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ServiceCreate

from core.models import Service


async def orm_create_service(
    session: AsyncSession, service_create: ServiceCreate
) -> Service:
    service = Service(**service_create.model_dump())
    session.add(service)
    await session.commit()
    await session.flush()
    return service


async def orm_get_services(session: AsyncSession):
    stmt = select(Service).order_by(Service.specialization_id)
    result = await session.scalars(stmt)
    return result.all()


async def orm_get_service(session: AsyncSession, service_id: int):
    stmt = select(Service).where(Service.id == service_id)
    return await session.scalar(stmt)
