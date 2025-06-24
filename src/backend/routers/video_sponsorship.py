from fastapi import APIRouter, Depends, Query
from typing import Optional
from backend.schemas.video_sponsorship import VideoSponsorshipRequest, VideoSponsorshipResponse
from pydantic import HttpUrl, ValidationError
from fastapi.exceptions import RequestValidationError
from backend.services.get_video_sponsorship import GetVideoSponsorshipService
from backend.core.session import session_dependency
from sqlalchemy.ext.asyncio import AsyncSession
from backend.logs.config import get_logger
from backend.schemas.sponsorship_flag import SponsorshipFlagPost, SponsorshipFlagPostResponse
from backend.services.flag_video_sponsorship import FlagVideoSponsorshipService
from pydantic import UUID4
from backend.repositories.all import (
    SponsoredSegmentRepository,
    VideoRepository,
    VideoMetadataRepository,
    GeneratedSponsorshipRepository,
    SponsorshipRepository,
    SponsorshipFlagRepository,
)

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


def get_flag_sponsorship_service() -> FlagVideoSponsorshipService:
    return FlagVideoSponsorshipService(
        SponsorshipRepository,
        SponsorshipFlagRepository,
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
    params: VideoSponsorshipRequest = Depends(parse_video_sponsorship_request),
    service: GetVideoSponsorshipService = Depends(get_video_service),
    session: AsyncSession = Depends(session_dependency),
):
    try:
        return await service.get_sponsorship_info(params, session)
    except Exception as e:
        logger.error(e)
        raise e


@router.post(
    "/videos/sponsorships/{sponsorship_id}/flag", response_model=SponsorshipFlagPostResponse
)
async def flag_sponsorship(
    sponsorship_id: UUID4,
    flag_details: SponsorshipFlagPost,
    service: FlagVideoSponsorshipService = Depends(get_flag_sponsorship_service),
    session: AsyncSession = Depends(session_dependency),
):
    try:
        return await service.flag_video_sponsorship(sponsorship_id, flag_details, session)
    except Exception as e:
        logger.error(e)
        raise e
