from fastapi import FastAPI
from sponsortrack.backend.core.config import settings
from sponsortrack.backend.api.v1.base import api_router
from sponsortrack.backend.db.models.all import Base  # noqa: F401


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    return app


app = start_application()


@app.get("/")
def hello_api():
    return {"msg": "Hello FastAPI🚀"}
