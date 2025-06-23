from backend.repositories.sponsorship import SponsorshipRepository
from backend.repositories.sponsorship_flag import SponsorshipFlagRepository
from backend.schemas.sponsorship_flag import SponsorshipFlagPost, SponsorshipFlagCreate
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from backend.models.sponsorship import Sponsorship


class FlagVideoSponsorshipService:
    def __init__(
        self,
        sponsorship_repo: SponsorshipRepository,
        flag_repo: SponsorshipFlagRepository,
    ):
        self.sponsorship_repo = sponsorship_repo()
        self.flag_repo = flag_repo()

    async def create_flag_add_data(
        self, sponsorship: Sponsorship, flag_details: SponsorshipFlagPost
    ) -> SponsorshipFlagCreate:
        return SponsorshipFlagCreate(
            flagged_field=flag_details.flagged_field,
            current_value=getattr(sponsorship, flag_details.flagged_field),
            corrected_value=flag_details.corrected_value,
            sponsorship_id=sponsorship.id,
        )

    async def flag_video_sponsorship(
        self, sponsorship_id: UUID4, flag_details: SponsorshipFlagPost, session: AsyncSession
    ):
        sponsorship = await self.sponsorship_repo.get_by_id(sponsorship_id, session)
        if not sponsorship:
            raise HTTPException(status_code=404, detail="No sponsorship found with id")

        flag_add_data = await self.create_flag_add_data(sponsorship, flag_details)
        flag = await self.flag_repo.add(flag_add_data, session)
        return flag
