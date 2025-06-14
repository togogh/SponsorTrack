from backend.repositories.video import VideoRepository
from pydantic import HttpUrl
from urllib.parse import urlparse, parse_qs
import requests
from backend.schemas.video_sponsorship import VideoSponsorshipRequest
from fastapi import HTTPException
from requests.adapters import HTTPAdapter, Retry
from backend.core.constants import constants
from backend.repositories.sponsored_segment import SponsoredSegmentRepository
from backend.mappers.sponsorblock_to_sponsored_segment import map_sponsorblock_to_sponsored_segment
from sqlalchemy.ext.asyncio import AsyncSession
from backend.mappers.youtube_id_to_video import map_youtube_id_to_video


class VideoSponsorshipService:
    def __init__(
        self, video_repo: VideoRepository, sponsored_segment_repo: SponsoredSegmentRepository
    ):
        self.video_repo: VideoRepository = video_repo()
        self.sponsored_segment_repo: SponsoredSegmentRepository = sponsored_segment_repo()

    async def extract_id_from_url(self, url: HttpUrl) -> str:
        parse_result = urlparse(str(url))

        # Extract video id from url
        try:
            if parse_result.path == "/watch":
                video_id = parse_qs(parse_result.query)["v"][0]
            elif parse_result.netloc == "youtu.be":
                video_id = parse_result.path.split("/")[1]
            elif parse_result.path.startswith("/embed/"):
                video_id = parse_result.path.split("/embed/")[1]
            elif parse_result.path.startswith("/shorts/"):
                video_id = parse_result.path.split("/shorts/")[1]
        except Exception:
            raise ValueError("Input url doesn't contain a valid video id")

        return video_id

    async def ensure_video_exists_on_youtube(self, video_id: str) -> str:
        # Check if video id belongs to an actual youtube video
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Video id doesn't exist on Youtube")
        except Exception:
            raise HTTPException(status_code=404, detail="Video id doesn't exist on Youtube")
        return video_id

    async def download_sponsorblock(self, video_id: str):
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

    async def get_sponsorship_info(self, params: VideoSponsorshipRequest, session: AsyncSession):
        youtube_id = params.id or await self.extract_id_from_url(params.url)

        # Get video from db, create if not there
        video = await self.video_repo.get_by_youtube_id(youtube_id, session)
        if not video:
            youtube_id = await self.ensure_video_exists_on_youtube(youtube_id)
            video_data = await map_youtube_id_to_video(youtube_id)
            video = await self.video_repo.add(video_data, session)

        # Get sponsored segments from db, create if not there
        sponsored_segments = await self.sponsored_segment_repo.get_by_video_id(youtube_id, session)
        if not sponsored_segments:
            blocks = await self.download_sponsorblock(youtube_id)
            sponsored_segments = []
            for block in blocks:
                block = await map_sponsorblock_to_sponsored_segment(block, video.id)
                sponsored_segment = await self.sponsored_segment_repo.add(block, session)
                sponsored_segments.append(sponsored_segment)

        # Get video metadata

        return sponsored_segments

        # return VideoSponsorshipResponse(**video)
