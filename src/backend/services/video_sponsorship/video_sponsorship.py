from backend.models.all import Sponsorship
from backend.repositories.all import (
    SponsoredSegmentRepository,
    VideoRepository,
    VideoMetadataRepository,
    GeneratedSponsorshipRepository,
    SponsorshipRepository,
)
from backend.schemas.all import (
    VideoSponsorshipRequest,
    VideoSponsorshipData,
    VideoSponsorshipResponse,
)
from .video import get_youtube_id, get_or_create_video
from .sponsorship import get_sponsorships, create_sponsorships
from .sponsored_segments import get_or_create_sponsored_segments, get_sponsored_segments
from .video_metadata import get_or_extract_metadata
from .transcript import ensure_subtitles_filled
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class VideoSponsorshipService:
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

    async def get_response(
        self, sponsorships: list[Sponsorship], youtube_id: str, session: AsyncSession
    ) -> VideoSponsorshipResponse:
        sponsorships_data = []
        for sponsorship in sponsorships:
            sponsored_segment = await get_sponsored_segments(
                session, self.sponsored_segment_repo, sponsorship_id=sponsorship.id
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

    async def get_video_sponsorships(self, params: VideoSponsorshipRequest, session: AsyncSession):
        youtube_id = await get_youtube_id(params.id, params.url)
        video = await get_or_create_video(youtube_id, self.video_repo, session)

        sponsorships = await get_sponsorships(video.id, self.sponsorship_repo, session)
        if not sponsorships:
            try:
                sponsored_segments = await get_or_create_sponsored_segments(
                    video, session, self.sponsored_segment_repo
                )
            except HTTPException as e:
                if e.status_code == 404:
                    response = await self.get_response([], youtube_id, session)
                    return response
                else:
                    raise e

            key_metadata, video_metadata = await get_or_extract_metadata(
                video, self.video_repo, self.video_metadata_repo, session
            )
            sponsored_segments = await ensure_subtitles_filled(
                sponsored_segments,
                video_metadata,
                video,
                self.sponsored_segment_repo,
                self.video_repo,
                self.video_metadata_repo,
                session,
            )
            sponsorships = await create_sponsorships(
                sponsored_segments,
                key_metadata,
                self.sponsorship_repo,
                self.generated_sponsorship_repo,
                session,
            )

        response = await self.get_response(sponsorships, youtube_id, session)
        return response
