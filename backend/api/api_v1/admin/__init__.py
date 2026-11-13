from fastapi import APIRouter, Depends

from api.api_v1.auth.validation import require_role
from common.enums.enums_db import RoleType
from core.config import settings

from .appointments import router as appointments_router

router = APIRouter(
    tags=["Admin"],
    dependencies=[Depends(require_role(RoleType.ADMIN))],
)

router.include_router(appointments_router, prefix=settings.api.v1.appointments)
