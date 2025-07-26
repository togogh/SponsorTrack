from fastapi import APIRouter, Depends, Query
from typing import Optional
from backend.core.session import session_dependency
from sqlalchemy.ext.asyncio import AsyncSession
from backend.logs.config import get_logger
from backend.schemas.flag import (
    SponsorshipFlagPost,
    SponsorshipFlagPostResponse,
    VideoFlagPost,
    VideoFlagPostResponse,
    SponsoredSegmentFlagPost,
    SponsoredSegmentFlagPostResponse,
    VideoFlagPostParams,
    SponsoredSegmentFlagPostParams,
)
from backend.services.flag import FlagService
from pydantic import UUID4
from backend.repositories.all import (
    SponsorshipRepository,
    FlagRepository,
    VideoRepository,
    SponsoredSegmentRepository,
)
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError

router = APIRouter()
logger = get_logger(__name__)


def get_flag_sponsorship_service() -> FlagService:
    return FlagService(
        SponsorshipRepository, VideoRepository, FlagRepository, SponsoredSegmentRepository
    )


def parse_video_flag_params(
    youtube_id: Optional[str] = Query(None),
    video_id: Optional[UUID4] = Query(None),
) -> VideoFlagPostParams:
    try:
        return VideoFlagPostParams(youtube_id=youtube_id, video_id=video_id)
    except ValidationError as e:
        logger.error(e)
        raise RequestValidationError(e.errors())


def parse_sponsored_segment_flag_params(
    sponsorship_id: Optional[str] = Query(None),
    sponsored_segment_id: Optional[UUID4] = Query(None),
) -> SponsoredSegmentFlagPostParams:
    try:
        return SponsoredSegmentFlagPostParams(
            sponsorship_id=sponsorship_id, sponsored_segment_id=sponsored_segment_id
        )
    except ValidationError as e:
        logger.error(e)
        raise RequestValidationError(e.errors())


@router.post("/videos/flag", response_model=VideoFlagPostResponse)
async def flag_video(
    flag_details: VideoFlagPost,
    params: VideoFlagPostParams = Depends(parse_video_flag_params),
    service: FlagService = Depends(get_flag_sponsorship_service),
    session: AsyncSession = Depends(session_dependency),
):
    try:
        return await service.flag_video(params, flag_details, session)
    except Exception as e:
        logger.error(e)
        raise e


@router.post("/videos/sponsorships/flag", response_model=SponsorshipFlagPostResponse)
async def flag_sponsorship(
    sponsorship_id: UUID4,
    flag_details: SponsorshipFlagPost,
    service: FlagService = Depends(get_flag_sponsorship_service),
    session: AsyncSession = Depends(session_dependency),
):
    try:
        return await service.flag_sponsorship(sponsorship_id, flag_details, session)
    except Exception as e:
        logger.error(e)
        raise e


@router.post(
    "/videos/sponsored-segments/flag",
    response_model=SponsoredSegmentFlagPostResponse,
)
async def flag_sponsored_segment(
    flag_details: SponsoredSegmentFlagPost,
    params: VideoFlagPostParams = Depends(parse_sponsored_segment_flag_params),
    service: FlagService = Depends(get_flag_sponsorship_service),
    session: AsyncSession = Depends(session_dependency),
):
    try:
        return await service.flag_sponsored_segment(params, flag_details, session)
    except Exception as e:
        logger.error(e)
        raise e
