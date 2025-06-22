from fastapi import APIRouter, Depends, Query
from typing import Optional
from backend.schemas.video_sponsorship import VideoSponsorshipRequest, VideoSponsorshipResponse
from pydantic import HttpUrl, ValidationError
from fastapi.exceptions import RequestValidationError
from backend.services.get_video_sponsorship import GetVideoSponsorshipService
from backend.repositories.video import VideoRepository
from backend.repositories.sponsored_segment import SponsoredSegmentRepository
from backend.core.session import session_dependency
from sqlalchemy.ext.asyncio import AsyncSession
from backend.repositories.video_metadata import VideoMetadataRepository
from backend.repositories.sponsorship import SponsorshipRepository
from backend.logs.config import get_logger
from backend.repositories.generated_sponsorship import GeneratedSponsorshipRepository


router = APIRouter()
logger = get_logger(__name__)


def get_video_service() -> GetVideoSponsorshipService:
    return GetVideoSponsorshipService(
        VideoRepository,
        SponsoredSegmentRepository,
        VideoMetadataRepository,
        SponsorshipRepository,
        GeneratedSponsorshipRepository,
    )


def parse_video_sponsorship_request(
    id: Optional[str] = Query(None),
    url: Optional[HttpUrl] = Query(None),
) -> VideoSponsorshipRequest:
    try:
        return VideoSponsorshipRequest(id=id, url=url)
    except ValidationError as e:
        logger.error(e)
        raise RequestValidationError(e.errors())


@router.get("/videos/sponsorships/", response_model=VideoSponsorshipResponse)
async def get_video_sponsorships(
    params: Optional[VideoSponsorshipRequest] = Depends(parse_video_sponsorship_request),
    service: GetVideoSponsorshipService = Depends(get_video_service),
    session: AsyncSession = Depends(session_dependency),
):
    try:
        return await service.get_sponsorship_info(params, session)
    except Exception as e:
        logger.error(e)
        raise e


# @router.post("/videos/sponsorships/{sponsorship_id}/flag")
# async def flag_sponsorship()
