from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429, content={"detail": "Rate limit exceeded. Please try again later."}
    )
