from backend.repositories.video import VideoRepository
from pydantic import HttpUrl
from urllib.parse import urlparse, parse_qs
import requests
from backend.schemas.video_sponsorship import VideoSponsorshipRequest
from fastapi import HTTPException
from requests.adapters import HTTPAdapter, Retry
from backend.core.constants import constants
from backend.repositories.sponsored_segment import SponsoredSegmentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.settings import ws_settings
import yt_dlp
from backend.repositories.video_metadata import VideoMetadataRepository
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api.formatters import JSONFormatter
import time
import json
from backend.mappers.video_sponsorship import VideoSponsorshipMapper
from backend.generators.get_generator import get_generator
import re
from backend.repositories.sponsorship import SponsorshipRepository
from backend.repositories.generated_sponsorship import GeneratedSponsorshipRepository


class GetVideoSponsorshipService:
    def __init__(
        self,
        video_repo: VideoRepository,
        sponsored_segment_repo: SponsoredSegmentRepository,
        video_metadata_repo: VideoMetadataRepository,
        sponsorship_repo: SponsorshipRepository,
        generated_sponsorship_repo: GeneratedSponsorshipRepository,
    ):
        self.video_repo: VideoRepository = video_repo()
        self.sponsored_segment_repo: SponsoredSegmentRepository = sponsored_segment_repo()
        self.video_metadata_repo: VideoMetadataRepository = video_metadata_repo()
        self.sponsorship_repo: SponsorshipRepository = sponsorship_repo()
        self.generated_sponsorship_repo: GeneratedSponsorshipRepository = (
            generated_sponsorship_repo()
        )
        self.mapper = VideoSponsorshipMapper()
        self.generator = get_generator()

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
            raise HTTPException(
                status_code=400, detail="Input url doesn't contain a valid video id"
            )

        try:
            return video_id
        except UnboundLocalError:
            raise HTTPException(
                status_code=400, detail="Input url doesn't contain a valid video id"
            )

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

    async def download_metadata(self, youtube_id):
        if ws_settings.WS_PROXY_UN and ws_settings.WS_PROXY_PW:
            proxy_str = (
                f"http://{ws_settings.WS_PROXY_UN}:{ws_settings.WS_PROXY_PW}@p.webshare.io:80/"
            )
        else:
            proxy_str = ""

        youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "no_warnings": True,
            "format_sort": ["+size", "+br", "+res", "+fps"],
            "fragment_retries": 10,
            "retries": 10,
            "no_cache_dir": True,
            "proxy": proxy_str,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove()
                info = ydl.extract_info(youtube_url, download=False)
                metadata = ydl.sanitize_info(info)
        except yt_dlp.utils.DownloadError:
            raise HTTPException(
                status_code=404,
                detail="Can't connect to yt_dlp",
            )

        return metadata

    async def fetch_transcript(self, youtube_id, language, retries=1, backoff_factor=0.1):
        if ws_settings.WS_PROXY_UN and ws_settings.WS_PROXY_PW:
            proxy_config = WebshareProxyConfig(
                proxy_username=ws_settings.WS_PROXY_UN,
                proxy_password=ws_settings.WS_PROXY_PW,
            )
            ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
        else:
            ytt_api = YouTubeTranscriptApi()
        if language is None:
            transcript_list = ytt_api.list(youtube_id)
            language = list(transcript_list)[0].language_code
        for r in range(retries):
            try:
                transcript = ytt_api.fetch(video_id=youtube_id, languages=[language])
                formatter = JSONFormatter()
                transcript = formatter.format_transcript(transcript, indent=4)
                transcript = json.loads(transcript)
                return transcript, language
            except Exception as e:
                print("Encountered error:", e)
                if r < retries:
                    print("Retrying...")
                    time.sleep(backoff_factor * (2 ** (r - 1)))

    async def extract_sponsor_info(self, prompt):
        self.generator.connect_client()
        self.generator.queue_message("user", prompt)
        self.generator.generate_response()
        response = self.generator.messages[-1]["content"]
        match = re.search(r"json\s*(\{.*?\})\s*", response, re.DOTALL)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            return data
        else:
            raise ValueError("No JSON found.")

    async def get_sponsorship_info(self, params: VideoSponsorshipRequest, session: AsyncSession):
        youtube_id = params.id or await self.extract_id_from_url(params.url)

        # Get video from db, create if not there
        video = await self.video_repo.get_by_youtube_id(youtube_id, session)
        if video:
            # Get sponsorships for video from db, create if not there
            sponsorships = await self.sponsorship_repo.get_by_video_id(video.id, session)
            if sponsorships:
                sponsorships_data = []
                for sponsorship in sponsorships:
                    sponsored_segment = await self.sponsored_segment_repo.get_by_sponsorship_id(
                        sponsorship.id, session
                    )
                    mapped_sponsorships_data = (
                        await self.mapper.map_segment_sponsorship_to_video_sponsorship_data(
                            sponsorship, sponsored_segment
                        )
                    )
                    sponsorships_data.append(mapped_sponsorships_data)
                response = await self.mapper.map_entities_to_response(sponsorships_data, video)
                return response
        else:
            youtube_id = await self.ensure_video_exists_on_youtube(youtube_id)
            mapped_video = await self.mapper.map_youtube_id_to_video(youtube_id)
            video = await self.video_repo.add(mapped_video, session)

        # Get sponsored segments from db, create if not there
        sponsored_segments = await self.sponsored_segment_repo.get_by_video_id(video.id, session)
        if not sponsored_segments:
            try:
                blocks = await self.download_sponsorblock(youtube_id)
            except HTTPException as e:
                if e.status_code == 404:
                    response = await self.mapper.map_entities_to_response([], video)
                    return response
                else:
                    raise e
            sponsored_segments = []
            for block in blocks:
                mapped_block = await self.mapper.map_sponsorblock_to_sponsored_segment(
                    block, video.id
                )
                sponsored_segment = await self.sponsored_segment_repo.add(mapped_block, session)
                sponsored_segments.append(sponsored_segment)

        # Get key metadata fields
        key_fields = ["language", "title", "upload_date", "description", "duration", "channel"]
        key_metadata = {field: getattr(video, field) for field in key_fields}
        if None in key_metadata.values():
            # Get video metadata, create if not there
            video_metadata = await self.video_metadata_repo.get_by_video_id(video.id, session)
            if not video_metadata:
                metadata_json = await self.download_metadata(youtube_id)
                mapped_metadata = await self.mapper.map_metadata_json_to_videometadata(
                    video.id, metadata_json
                )
                video_metadata = await self.video_metadata_repo.add(mapped_metadata, session)

            key_metadata = {field: video_metadata.raw_json.get(field) for field in key_fields}
            mapped_key_metadata = await self.mapper.map_key_metadata_to_video(key_metadata)
            await self.video_repo.update(video.id, mapped_key_metadata, session)

        # Check segment subtitles, fetch if null
        empty_subtitles_segments = [
            segment.id for segment in sponsored_segments if segment.subtitles is None
        ]
        if len(empty_subtitles_segments) > 0:
            try:
                transcript = video_metadata.raw_transcript
            except UnboundLocalError:
                video_metadata = await self.video_metadata_repo.get_by_video_id(video.id, session)
                transcript = video_metadata.raw_transcript
            if transcript is None:
                transcript, transcript_language = await self.fetch_transcript(
                    youtube_id, video.language
                )
                if video.language is None:
                    mapped_language_metadata = await self.mapper.map_language_metadata_to_video(
                        transcript_language
                    )
                    await self.video_repo.update(video.id, mapped_language_metadata, session)
                mapped_transcript = await self.mapper.map_metadata_transcript_to_videometadata(
                    transcript
                )
                await self.video_metadata_repo.update(video_metadata.id, mapped_transcript, session)
            for segment in sponsored_segments:
                segment.subtitles = await self.mapper.map_transcript_to_segment_subtitles(
                    transcript, segment
                )
                mapped_segment = await self.mapper.map_subtitles_to_sponsoredsegment(
                    segment.subtitles
                )
                await self.sponsored_segment_repo.update(segment.id, mapped_segment, session)

        sponsorships_data = []
        for sponsored_segment in sponsored_segments:
            prompt = await self.mapper.map_metadata_to_prompt(video, sponsored_segment)
            sponsorship = await self.extract_sponsor_info(prompt)
            mapped_sponsorship = await self.mapper.map_sponsorship_data_to_sponsorship(
                sponsorship, sponsored_segment.id
            )
            sponsorship = await self.sponsorship_repo.add(mapped_sponsorship, session)
            mapped_generated_sponsorship = (
                await self.mapper.map_sponsorship_to_generated_sponsorship(sponsorship)
            )
            await self.generated_sponsorship_repo.add(mapped_generated_sponsorship, session)
            mapped_sponsorships_data = (
                await self.mapper.map_segment_sponsorship_to_video_sponsorship_data(
                    sponsorship, sponsored_segment
                )
            )
            sponsorships_data.append(mapped_sponsorships_data)

        response = await self.mapper.map_entities_to_response(sponsorships_data, video)

        return response
