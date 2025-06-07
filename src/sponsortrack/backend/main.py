from fastapi import FastAPI
from sponsortrack.backend.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


@app.get("/")
def hello_api():
    return {"msg": "Hello FastAPI🚀"}
