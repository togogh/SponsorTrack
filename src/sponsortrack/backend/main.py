from fastapi import FastAPI
from sponsortrack.backend.core.config import settings
from sponsortrack.backend.api.v1.base import api_router
from sponsortrack.backend.db.models.all import Base  # noqa: F401
from sponsortrack.backend.core.limiting import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sponsortrack.backend.core.exceptions import rate_limit_exceeded_handler


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    include_router(app)
    return app


app = start_application()
