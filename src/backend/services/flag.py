from backend.repositories.all import FlagRepository, SponsorshipRepository, VideoRepository
from backend.schemas.flag import (
    SponsorshipFlagPost,
    SponsorshipFlagCreate,
    VideoFlagCreate,
    VideoFlagPost,
)
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from backend.models.all import Sponsorship, Video


class FlagService:
    def __init__(
        self,
        sponsorship_repo: SponsorshipRepository,
        video_repo: VideoRepository,
        flag_repo: FlagRepository,
    ):
        self.sponsorship_repo: SponsorshipRepository = sponsorship_repo()
        self.video_repo: VideoRepository = video_repo()
        self.flag_repo: FlagRepository = flag_repo()

    async def get_sponsorship_flag_create_data(
        self, sponsorship: Sponsorship, flag_details: SponsorshipFlagPost
    ) -> SponsorshipFlagCreate:
        return SponsorshipFlagCreate(
            field_flagged=flag_details.field_flagged,
            value_flagged=getattr(sponsorship, flag_details.field_flagged),
            entity_id=sponsorship.id,
        )

    async def get_video_flag_create_data(
        self, video: Video, flag_details: VideoFlagPost, session: AsyncSession
    ) -> VideoFlagCreate:
        if flag_details.field_flagged == "num_sponsored_segments":
            sponsorships = self.sponsorship_repo.get_by_video_id(video.id, session)
            num_sponsored_segments = len(sponsorships)
            current_value = num_sponsored_segments
        else:
            current_value = getattr(video, flag_details.field_flagged)
        return VideoFlagCreate(
            field_flagged=flag_details.field_flagged,
            current_value=current_value,
            entity_id=video.id,
        )

    async def flag_sponsorship(
        self, sponsorship_id: UUID4, flag_details: SponsorshipFlagPost, session: AsyncSession
    ):
        sponsorship = await self.sponsorship_repo.get_by_id(sponsorship_id, session)
        if not sponsorship:
            raise HTTPException(status_code=404, detail="No sponsorship found with id")

        flag_add_data = await self.get_sponsorship_flag_create_data(sponsorship, flag_details)
        flag = await self.flag_repo.add("sponsorship", flag_add_data, session)
        return flag

    async def flag_video(self, video_id: UUID4, flag_details: VideoFlagPost, session: AsyncSession):
        video = await self.video_repo.get_by_id(video_id, session)
        if not video:
            raise HTTPException(status_code=404, detail="No video found with id")

        flag_add_data = await self.get_video_flag_create_data(video, flag_details)
        flag = await self.flag_repo.add("video", flag_add_data, session)
        return flag
