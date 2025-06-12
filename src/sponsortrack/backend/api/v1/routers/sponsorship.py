from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sponsortrack.backend.db.session import get_session
from sponsortrack.backend.schemas.sponsorship import SponsorshipRequest
from sponsortrack.backend.services.video import Video


router = APIRouter()


@router.get("/sponsorship/")
async def get_sponsorship(
    request: Request,
    sponsorship_request: SponsorshipRequest,
    session: Session = Depends(get_session),
):
    sponsorship = SponsorshipRepository.create_user(
        sponsorship_request=sponsorship_request, session=session
    )
    return sponsorship
