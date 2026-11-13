from fastapi import APIRouter

from core.config import settings

from .appointments import router as appointments_router

router = APIRouter(tags=["Admin"])

router.include_router(appointments_router, prefix=settings.api.v1.appointments)
