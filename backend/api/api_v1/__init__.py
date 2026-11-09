from fastapi import APIRouter

from core.config import settings

from .users.views import router as users_router
from .auth.views import router as auth_router
from .specializations.views import router as specialization_router
from .cabinets.views import router as cabintes_router
from .services.views import router as services_router
from .doctors.views import router as doctors_router
from .schedules.work_schedules_views import router as schedules_router
from .schedules.schedules_exception_views import router as schedules_exception_router
from .slots.views import router as slots_router
from .patients.views import router as patients_router
from .appointments.views import router as appointments_router

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(users_router, prefix=settings.api.v1.users)
router.include_router(auth_router, prefix=settings.api.v1.auth)
router.include_router(specialization_router, prefix=settings.api.v1.specializations)
router.include_router(cabintes_router, prefix=settings.api.v1.cabinets)
router.include_router(services_router, prefix=settings.api.v1.services)
router.include_router(doctors_router, prefix=settings.api.v1.doctors)
router.include_router(schedules_router, prefix=settings.api.v1.work_schedules)
router.include_router(
    schedules_exception_router, prefix=settings.api.v1.schedules_exception
)
router.include_router(slots_router, prefix=settings.api.v1.slots)
router.include_router(patients_router, prefix=settings.api.v1.patients)
router.include_router(appointments_router, prefix=settings.api.v1.appointments)
