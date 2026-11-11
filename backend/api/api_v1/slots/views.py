from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.slots.service import get_available_slots
from core.db_helper import db_helper

from .schemas import SlotRead

router = APIRouter(tags=["Slots"])


@router.get("/", response_model=list[SlotRead])
async def get_slots(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    service_id: int = Query(),
    doctor_id: int = Query(),
    date: date = Query(),
):
    return await get_available_slots(
        session=session, doctor_id=doctor_id, service_id=service_id, target_date=date
    )
