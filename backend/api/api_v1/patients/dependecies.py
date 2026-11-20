from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.patients.crud import orm_get_patient
from core.db_helper import db_helper


async def patient_by_id(
    patient_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    patient = await orm_get_patient(session=session, user_id=patient_id)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The questionnaire is not filled out",
        )
    return patient
