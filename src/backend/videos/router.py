from fastapi import APIRouter, Depends, Query
from typing import Optional
from .schema import VideoSponsorshipRequest
from pydantic import HttpUrl, ValidationError
from fastapi.exceptions import RequestValidationError
from .service import VideoService
from .repository import VideoRepository

router = APIRouter()


def get_video_service() -> VideoService:
    return VideoService(VideoRepository)


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
    service: VideoService = Depends(get_video_service),
):
    return service.get_sponsorship_info(params)
