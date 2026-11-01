from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def orm_get_users(session: AsyncSession):
    stmt = select(User).order_by(User.id).where(User.is_active == True)
    result = await session.scalars(stmt)
    return result.all()
