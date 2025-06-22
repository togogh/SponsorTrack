from backend.repositories.sponsorship import SponsorshipRepository


class FlagVideoSponsorshipService:
    def __init__(
        self,
        sponsorship_repo: SponsorshipRepository,
    ):
        self.sponsorship_repo = sponsorship_repo

    # async def flag_video_sponsorship(self):
