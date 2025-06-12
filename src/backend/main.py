from fastapi import FastAPI
from backend.videos.router import router as videos_router

app = FastAPI()

app.include_router(videos_router, tags=["videos"])
