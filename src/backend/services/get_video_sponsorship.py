from .generators.get_generator import get_generator
from .generators.base_generator import BaseGenerator
from .youtube import (
    extract_id_from_url,
    download_metadata,
    fetch_transcript,
    map_transcript_to_segment_subtitles,
)
from .sponsorblock import download_sponsorblock
from backend.core.settings import generator_settings
from backend.models.all import Video, Sponsorship, SponsoredSegment, VideoMetadata
from backend.repositories.all import (
    SponsoredSegmentRepository,
    VideoRepository,
    VideoMetadataRepository,
    GeneratedSponsorshipRepository,
    SponsorshipRepository,
)
from backend.schemas.video import VideoCreate, VideoUpdate
from backend.schemas.video_sponsorship import (
    VideoSponsorshipRequest,
    VideoSponsorshipData,
    VideoSponsorshipResponse,
)
from backend.schemas.sponsored_segment import SponsoredSegmentCreate, SponsoredSegmentUpdate
from backend.schemas.video_metadata import VideoMetadataCreate, VideoMetadataUpdate
from backend.schemas.sponsorship import SponsorshipCreate
from backend.schemas.generated_sponsorship import GeneratedSponsorshipCreate
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple
from pydantic import UUID4
from datetime import datetime


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
        self.generator: BaseGenerator = get_generator()

    async def get_youtube_id(self, params: VideoSponsorshipRequest) -> str:
        return params.id or await extract_id_from_url(params.url)

    async def create_video(self, youtube_id: str, session: AsyncSession) -> Video:
        video_create_data = VideoCreate(youtube_id=youtube_id)
        video = await self.video_repo.add(video_create_data, session)
        return video

    async def get_or_create_video(self, youtube_id: str, session: AsyncSession) -> Video:
        video = await self.video_repo.get_by_youtube_id(youtube_id, session)
        if not video:
            video = await self.create_video(youtube_id, session)
        return video

    async def get_sponsorships(self, video_id: UUID4, session: AsyncSession) -> list[Sponsorship]:
        sponsorships = await self.sponsorship_repo.get_by_video_id(video_id, session)
        return sponsorships

    async def get_sponsored_segments(
        self, session: AsyncSession, sponsorship_id: UUID4 = None, video_id: UUID4 = None
    ) -> list[SponsoredSegment]:
        if sponsorship_id and video_id:
            raise ValueError("Only provide one kind of id.")

        if sponsorship_id:
            segments = await self.sponsored_segment_repo.get_by_sponsorship_id(
                sponsorship_id, session
            )
        elif video_id:
            segments = await self.sponsored_segment_repo.get_by_video_id(video_id, session)
        else:
            raise ValueError("At least one id must be given.")

        return segments

    async def get_or_create_sponsored_segments(
        self, video: Video, session: AsyncSession
    ) -> list[SponsoredSegment]:
        sponsored_segments = await self.get_sponsored_segments(video.id, session)
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
                    duration=block["segment"][1] - block["segment"][0],
                    parent_video_id=video.id,
                )
                sponsored_segment = await self.sponsored_segment_repo.add(
                    sponsored_segment_create, session
                )
                sponsored_segments.append(sponsored_segment)
        return sponsored_segments

    async def get_or_create_video_metadata(
        self, video: Video, session: AsyncSession
    ) -> VideoMetadata:
        # Get video metadata, create if not there
        video_metadata = await self.video_metadata_repo.get_by_video_id(video.id, session)
        if not video_metadata:
            metadata_json = await download_metadata(video.youtube_id)
            video_metadata_create = VideoMetadataCreate(
                raw_json=metadata_json,
                video_id=video.id,
            )
            video_metadata = await self.video_metadata_repo.add(video_metadata_create, session)
        return video_metadata

    async def get_or_extract_metadata(
        self, video: Video, session: AsyncSession
    ) -> Tuple[dict, VideoMetadata]:
        video_metadata = self.get_or_create_video_metadata(video, session)
        key_fields = ["language", "title", "upload_date", "description", "duration", "channel"]
        key_metadata = {field: getattr(video, field) for field in key_fields}
        if None in key_metadata.values():
            key_metadata = {field: video_metadata.raw_json.get(field) for field in key_fields}
            video_update = VideoUpdate(
                language=video_metadata["language"],
                title=video_metadata["title"],
                upload_date=datetime.strptime(video_metadata["upload_date"], "%Y%m%d"),
                description=video_metadata["description"],
                duration=video_metadata["duration"],
                channel=video_metadata["channel"],
            )
            await self.video_repo.update(video.id, video_update, session)
        return key_metadata, video_metadata

    async def get_or_fill_transcript(
        self, video_metadata: VideoMetadata, video: Video, session: AsyncSession
    ) -> dict:
        transcript = video_metadata.raw_transcript
        if transcript is None:
            transcript, transcript_language = await fetch_transcript(
                video.youtube_id, video.language
            )
            if video.language is None or len(video.language) > 2:
                video_update = VideoUpdate(
                    language=transcript_language,
                )
                await self.video_repo.update(video.id, video_update, session)
            video_metadata_update = VideoMetadataUpdate(
                raw_transcript=transcript,
            )
            await self.video_metadata_repo.update(video_metadata.id, video_metadata_update, session)
        return transcript

    async def ensure_subtitles_filled(
        self,
        sponsored_segments: list[SponsoredSegment],
        video_metadata: VideoMetadata,
        video: Video,
        session: AsyncSession,
    ) -> list[SponsoredSegment]:
        empty_subtitles_segments = [
            segment.id for segment in sponsored_segments if segment.subtitles is None
        ]
        if len(empty_subtitles_segments) > 0:
            transcript = await self.get_or_fill_transcript(video_metadata, video, session)
            for segment in sponsored_segments:
                segment.subtitles = await map_transcript_to_segment_subtitles(transcript, segment)
                sponsored_segment_update = SponsoredSegmentUpdate(subtitles=segment.subtitles)
                await self.sponsored_segment_repo.update(
                    segment.id, sponsored_segment_update, session
                )
        return sponsored_segments

    async def create_prompt(self, metadata, segment):
        prompt = f"""
            I have a sponsored segment cut from a Youtube video. Here's some information about this segment:

            Youtube channel: {metadata["channel"]}
            Video description: {metadata["description"]}
            Upload date: {metadata["upload_date"]}
            Video language: {metadata["language"]}
            Segment subtitles: {segment.subtitles}

            The subtitles can be auto-generated, so don't assume what's written there is the absolute truth, especially the spelling. Double check the information there using the other fields.

            Given this information, could you give me information about the sponsor? I want you to return a json with the following information:

            sponsor_name: Sponsor's name
            sponsor_description: Sponsor's products and services
            sponsor_offer: The specific discount or promo provided by the sponsor, if any
            sponsor_links: List of hyperlinks related to the sponsor, such as affiliate links, homepages, or links to the offer, if any.
            sponsor_coupon_code: Coupon code, if any

            Please respond with the json enclosed in a ```json ``` markdown code block.
        """
        return prompt

    async def create_sponsorships(
        self, sponsored_segments: list[SponsoredSegment], metadata: dict, session: AsyncSession
    ) -> list[Sponsorship]:
        sponsorships = []
        for sponsored_segment in sponsored_segments:
            prompt = await self.create_prompt(metadata, sponsored_segment)
            sponsorship = await self.generator.extract_sponsor_info(prompt)
            sponsorship_create = SponsorshipCreate(
                sponsor_name=sponsorship["sponsor_name"],
                sponsor_description=sponsorship["sponsor_description"],
                sponsor_links=sponsorship["sponsor_links"],
                sponsor_coupon_code=sponsorship["sponsor_coupon_code"],
                sponsor_offer=sponsorship["sponsor_offer"],
                sponsored_segment_id=sponsored_segment.id,
            )
            sponsorship = await self.sponsorship_repo.add(sponsorship_create, session)
            generated_sponsorship_create = GeneratedSponsorshipCreate(
                sponsor_name=sponsorship.sponsor_name,
                sponsor_description=sponsorship.sponsor_description,
                sponsor_links=sponsorship.sponsor_links,
                sponsor_coupon_code=sponsorship.sponsor_coupon_code,
                sponsor_offer=sponsorship.sponsor_offer,
                sponsorship_id=sponsorship.id,
                generator=generator_settings.GENERATOR,
                provider=generator_settings.PROVIDER,
                model=generator_settings.MODEL,
            )
            await self.generated_sponsorship_repo.add(generated_sponsorship_create, session)
            sponsorships.append(sponsorship)
        return sponsorships

    async def get_response(
        self, sponsorships: list[Sponsorship], youtube_id: str, session: AsyncSession
    ) -> VideoSponsorshipResponse:
        sponsorships_data = []
        for sponsorship in sponsorships:
            sponsored_segment = await self.get_sponsored_segments(
                session, sponsorship_id=sponsorship.id
            )
            video_sponsorship_data = VideoSponsorshipData(
                id=sponsorship.id,
                start_time=sponsored_segment.start_time,
                end_time=sponsored_segment.end_time,
                sponsor_name=sponsorship.sponsor_name,
                sponsor_description=sponsorship.sponsor_description,
                sponsor_links=sponsorship.sponsor_links,
                sponsor_coupon_code=sponsorship.sponsor_coupon_code,
                sponsor_offer=sponsorship.sponsor_offer,
            )
            sponsorships_data.append(video_sponsorship_data)
        response = VideoSponsorshipResponse(youtube_id=youtube_id, sponsorships=sponsorships_data)
        return response

    async def get_sponsorship_info(self, params: VideoSponsorshipRequest, session: AsyncSession):
        youtube_id = await self.get_youtube_id(params)
        video = await self.get_or_create_video(youtube_id, session)

        sponsorships = await self.get_sponsorships(video.id, session)
        if not sponsorships:
            try:
                sponsored_segments = await self.get_or_create_sponsored_segments(video.id, session)
            except HTTPException as e:
                if e.status_code == 404:
                    response = await self.get_response([], youtube_id)
                    return response
                else:
                    raise e

            key_metadata, video_metadata = self.get_or_extract_metadata(video, session)
            sponsored_segments = self.ensure_subtitles_filled(
                sponsored_segments, video_metadata, video, session
            )
            sponsorships = self.create_sponsorships(sponsored_segments, key_metadata, session)

        response = await self.get_response(sponsorships, youtube_id)
        return response
