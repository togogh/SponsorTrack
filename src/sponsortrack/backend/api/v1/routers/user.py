from fastapi import APIRouter, status, Request
from sqlalchemy.orm import Session
from fastapi import Depends

from sponsortrack.backend.schemas.user import UserCreate, UserShow
from sponsortrack.backend.db.session import get_session
from sponsortrack.backend.db.repositories.user import UserRepository

from sponsortrack.backend.core.limiting import limiter

router = APIRouter()


@router.post("/user/", response_model=UserShow, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_user(request: Request, user: UserCreate, session: Session = Depends(get_session)):
    user = UserRepository.create_user(user=user, session=session)
    return user
