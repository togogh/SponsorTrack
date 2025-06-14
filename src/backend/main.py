from fastapi import FastAPI
from backend.routers.video_sponsorship import router as video_sponsorship_router
from backend.models.all import Base  # noqa: F401

app = FastAPI()

app.include_router(video_sponsorship_router, tags=["video_sponsorships"])
