from fastapi import FastAPI
from backend.routers.all import router
from backend.models.all import Base  # noqa: F401
from backend.logs.config import get_logger

app = FastAPI()
get_logger("uvicorn.error")
get_logger("uvicorn.access")
get_logger("sqlalchemy.engine.Engine")

app.include_router(router)
