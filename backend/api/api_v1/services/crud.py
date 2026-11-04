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
