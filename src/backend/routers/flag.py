from fastapi import APIRouter, Depends
from backend.core.session import session_dependency
from sqlalchemy.ext.asyncio import AsyncSession
from backend.logs.config import get_logger
from backend.schemas.flag import (
    SponsorshipFlagPost,
    SponsorshipFlagPostResponse,
    VideoFlagPost,
    VideoFlagPostResponse,
)
from backend.services.flag import FlagService
from pydantic import UUID4
from backend.repositories.all import SponsorshipRepository, FlagRepository, VideoRepository

router = APIRouter()
logger = get_logger(__name__)


def get_flag_sponsorship_service() -> FlagService:
    return FlagService(SponsorshipRepository, VideoRepository, FlagRepository)


@router.post("/videos/{video_id}/flag", response_model=VideoFlagPostResponse)
async def flag_video(
    video_id: UUID4,
    flag_details: VideoFlagPost,
    service: FlagService = Depends(get_flag_sponsorship_service),
    session: AsyncSession = Depends(session_dependency),
):
    try:
        return await service.flag_video(video_id, flag_details, session)
    except Exception as e:
        logger.error(e)
        raise e


@router.post(
    "/videos/sponsorships/{sponsorship_id}/flag", response_model=SponsorshipFlagPostResponse
)
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
