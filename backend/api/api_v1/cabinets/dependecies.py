from logging import getLogger
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import orm_get_cabinet
from core.db_helper import db_helper
from core.models import Cabinet

logger = getLogger(__name__)


async def cabinet_by_id(
    cabinet_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Cabinet:
    cabinet = await orm_get_cabinet(session=session, cabinet_id=cabinet_id)
    if cabinet is not None:
        return cabinet
    logger.warning(f"Cabinet {cabinet_id} not found")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Cabinet not found"
    )
