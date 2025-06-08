from sqlalchemy.orm import Session

from sponsortrack.backend.schemas.user import UserCreate
from sponsortrack.backend.db.models.user import User
from sponsortrack.backend.core.hashing import Hasher


class UserRepository:
    def create_user(user: UserCreate, session: Session):
        user = User(
            username=user.username,
            email=user.email,
            password=Hasher.get_password_hash(user.password.get_secret_value()),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
