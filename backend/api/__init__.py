from fastapi import APIRouter

from api_v1 import router as api_v1_rotuer

router = APIRouter()
router.include_router(api_v1_rotuer)
