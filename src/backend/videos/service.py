from .repository import VideoRepository
from pydantic import HttpUrl
from urllib.parse import urlparse, parse_qs
import requests
from .schema import VideoSponsorshipResponse, VideoSponsorshipRequest
from fastapi import HTTPException


class VideoService:
    def __init__(self, repo: VideoRepository):
        self.repo = repo()

    def extract_id_from_url(self, url: HttpUrl) -> str:
        parse_result = urlparse(url)

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

    def ensure_video_exists_on_youtube(self, video_id: str) -> str:
        # Check if video id belongs to an actual youtube video
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Video id doesn't exist on Youtube")
        except Exception:
            raise HTTPException(status_code=404, detail="Video id doesn't exist on Youtube")
        return video_id

    def get_sponsorship_info(self, params: VideoSponsorshipRequest) -> VideoSponsorshipResponse:
        youtube_id = params.id or self.extract_id_from_url(params.url)

        data = self.repo.get_video_sponsorship(youtube_id)

        if not data:
            youtube_id = self.ensure_video_exists_on_youtube(youtube_id)

        return VideoSponsorshipResponse(**data)
