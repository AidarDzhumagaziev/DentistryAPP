from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.users.schemas import UserAdminCreate, UserCreate

from core.models import User


async def orm_create_user(
    session: AsyncSession,
    user_create: UserCreate | UserAdminCreate,
    role_id: int,
    password_hash: bytes,
) -> User:
    user = User(
        email=user_create.email,
        phone=user_create.phone,
        password_hash=password_hash,
        role_id=role_id,
        full_name=user_create.full_name,
    )
    session.add(user)
    await session.flush()
    await session.commit()
    return user
