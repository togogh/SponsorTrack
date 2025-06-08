from fastapi import APIRouter, status
from sqlalchemy.orm import Session
from fastapi import Depends

from sponsortrack.backend.schemas.user import UserCreate, UserShow
from sponsortrack.backend.db.session import get_session
from sponsortrack.backend.db.repositories.user import UserRepository

router = APIRouter()


@router.post("/users/", response_model=UserShow, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    user = UserRepository.create_user(user=user, session=session)
    return user
