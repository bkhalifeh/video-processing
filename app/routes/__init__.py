from fastapi import APIRouter
from .video import router as video_router

router = APIRouter(prefix="/api")
router.include_router(video_router)
