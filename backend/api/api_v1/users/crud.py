from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import User


async def orm_get_users(session: AsyncSession):
    stmt = select(User).order_by(User.id).where(User.is_active == True)
    result = await session.scalars(stmt)
    return result.all()


async def orm_get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).options(selectinload(User.role)).where(User.email == email)
    return await session.scalar(stmt)


async def orm_get_user_by_phone(session: AsyncSession, phone: str) -> User | None:
    stmt = select(User).where(User.phone == phone)
    return await session.scalar(stmt)


async def orm_get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).options(selectinload(User.role)).where(User.id == user_id)
    return await session.scalar(stmt)
