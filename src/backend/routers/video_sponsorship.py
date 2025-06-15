from fastapi import APIRouter, Depends, Query
from typing import Optional
from backend.schemas.video_sponsorship import VideoSponsorshipRequest
from pydantic import HttpUrl, ValidationError
from fastapi.exceptions import RequestValidationError
from backend.services.video_sponsorship import VideoSponsorshipService
from backend.repositories.video import VideoRepository
from backend.repositories.sponsored_segment import SponsoredSegmentRepository
from backend.core.session import session_dependency
from sqlalchemy.ext.asyncio import AsyncSession
from backend.repositories.video_metadata import VideoMetadataRepository


router = APIRouter()


def get_video_service() -> VideoSponsorshipService:
    return VideoSponsorshipService(
        VideoRepository, SponsoredSegmentRepository, VideoMetadataRepository
    )


def parse_video_sponsorship_request(
    id: Optional[str] = Query(None),
    url: Optional[HttpUrl] = Query(None),
) -> VideoSponsorshipRequest:
    try:
        return VideoSponsorshipRequest(id=id, url=url)
    except ValidationError as e:
        raise RequestValidationError(e.errors())


@router.get("/videos/sponsorships/")
async def get_video_sponsorships(
    params: Optional[VideoSponsorshipRequest] = Depends(parse_video_sponsorship_request),
    service: VideoSponsorshipService = Depends(get_video_service),
    session: AsyncSession = Depends(session_dependency),
):
    return await service.get_sponsorship_info(params, session)
