from .flag import router as flag_router
from .video_sponsorship import router as video_sponsorship_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(video_sponsorship_router, tags=["video_sponsorship"])
router.include_router(flag_router, tags=["flag"])
