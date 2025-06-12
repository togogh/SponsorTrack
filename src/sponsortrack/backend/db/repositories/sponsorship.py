from sqlalchemy.orm import Session

from sponsortrack.backend.schemas.sponsorship import SponsorshipRequest
from sponsortrack.backend.db.models.video import Video


class SponsorshipRepository:
    def create_user(sponsorship_request: SponsorshipRequest, session: Session):
        sponsorship_request = Video()
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
