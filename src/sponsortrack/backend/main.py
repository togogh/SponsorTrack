from fastapi import FastAPI
from sponsortrack.backend.core.config import settings
from sponsortrack.backend.db.session import get_remote_engine


def start_application(engine):
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    return app


with get_remote_engine() as engine:
    app = start_application(engine)


@app.get("/")
def hello_api():
    return {"msg": "Hello FastAPI🚀"}
