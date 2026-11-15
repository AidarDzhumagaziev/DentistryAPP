from fastapi import APIRouter, Depends

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType
from core.config import settings

from .appointments import router as appointments_router
from .patients import router as patients_router

router = APIRouter(
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)

router.include_router(appointments_router, prefix=settings.api.v1.appointments)
router.include_router(patients_router, prefix=settings.api.v1.patients)
