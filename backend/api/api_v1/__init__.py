from fastapi import APIRouter

from core.config import settings

from .users.views import router as users_router
from .auth.views import router as auth_router
from .specializations.views import router as specialization_router
from .cabinets.views import router as cabintes_router

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(users_router, prefix=settings.api.v1.users)
router.include_router(auth_router, prefix=settings.api.v1.auth)
router.include_router(specialization_router, prefix=settings.api.v1.specializations)
router.include_router(cabintes_router, prefix=settings.api.v1.cabinets)
