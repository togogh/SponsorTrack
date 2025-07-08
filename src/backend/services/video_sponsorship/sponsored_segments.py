import requests
from requests.adapters import HTTPAdapter, Retry
from backend.core.constants import constants
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from backend.schemas.all import SponsoredSegmentCreate
from backend.models.all import Video, SponsoredSegment
from backend.repositories.all import SponsoredSegmentRepository


async def download_sponsorblock(video_id: str) -> dict:
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

    s.mount("https://", HTTPAdapter(max_retries=retries))
    url = f"{constants.SPONSORBLOCK_BASE_URL}/api/skipSegments?videoID={video_id}"

    response = s.get(url)
    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="This video has no sponsored segments marked with Sponsorblock. If this is a mistake, add them with https://sponsor.ajay.app/",
        )
    else:
        raise HTTPException(status_code=503, detail="Can't connect to Sponsorblock")

    return data


async def get_sponsored_segments(
    session: AsyncSession,
    sponsored_segment_repo: SponsoredSegmentRepository,
    sponsorship_id: UUID4 = None,
    video_id: UUID4 = None,
) -> list[SponsoredSegment]:
    if sponsorship_id and video_id:
        raise ValueError("Only provide one kind of id.")

    if sponsorship_id:
        segments = await sponsored_segment_repo.get_by_sponsorship_id(sponsorship_id, session)
    elif video_id:
        segments = await sponsored_segment_repo.get_by_video_id(video_id, session)
    else:
        raise ValueError("At least one id must be given.")

    return segments


async def get_or_create_sponsored_segments(
    video: Video, session: AsyncSession, sponsored_segment_repo: SponsoredSegmentRepository
) -> list[SponsoredSegment]:
    sponsored_segments = await get_sponsored_segments(
        session, sponsored_segment_repo, video_id=video.id
    )
    if not sponsored_segments:
        try:
            blocks = await download_sponsorblock(video.youtube_id)
        except Exception as e:
            raise e
        sponsored_segments = []
        for block in blocks:
            sponsored_segment_create = SponsoredSegmentCreate(
                sponsorblock_id=block["UUID"],
                start_time=block["segment"][0],
                end_time=block["segment"][1],
                parent_video_id=video.id,
            )
            sponsored_segment = await sponsored_segment_repo.add(sponsored_segment_create, session)
            sponsored_segments.append(sponsored_segment)
    return sponsored_segments
