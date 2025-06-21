from fastapi import FastAPI
from backend.routers.video_sponsorship import router as video_sponsorship_router
from backend.models.all import Base  # noqa: F401
from backend.core.logging_config import get_logger

app = FastAPI()
get_logger("uvicorn.error")
get_logger("uvicorn.access")
get_logger("sqlalchemy.engine.Engine")

app.include_router(video_sponsorship_router, tags=["video_sponsorships"])
