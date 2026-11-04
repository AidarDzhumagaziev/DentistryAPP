from logging import getLogger
from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import orm_get_specialization

from core.db_helper import db_helper

logger = getLogger(__name__)


async def specialization_by_id(
    spec_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    specialization = await orm_get_specialization(
        session=session, specialization_id=spec_id
    )
    if specialization is not None:
        return specialization
    logger.warning(f"Specialization {spec_id} not found")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Specialization not found",
    )
