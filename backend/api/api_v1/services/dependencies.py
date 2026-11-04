from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper

from .crud import orm_get_service


async def service_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service_id: Annotated[int, Path],
):
    service = await orm_get_service(session=session, service_id=service_id)
    if service is not None:
        return service
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
    )
