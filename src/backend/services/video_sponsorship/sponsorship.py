from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.all import Sponsorship, SponsoredSegment
from backend.repositories.all import SponsorshipRepository, GeneratedSponsorshipRepository
from backend.schemas.all import KeyMetadata, SponsorshipCreate, GeneratedSponsorshipCreate
from backend.services.generators.get_generator import get_generator
from backend.core.settings import generator_settings


async def get_sponsorships(
    video_id: UUID4, sponsorship_repo: SponsorshipRepository, session: AsyncSession
) -> list[Sponsorship]:
    sponsorships = await sponsorship_repo.get_by_video_id(video_id, session)
    return sponsorships


async def create_prompt(metadata: KeyMetadata, segment: SponsoredSegment):
    prompt = f"""
        I have a sponsored segment cut from a Youtube video. Here's some information about this segment:

        Youtube channel: {metadata.channel}
        Video description: {metadata.description}
        Upload date: {metadata.upload_date}
        Video language: {metadata.language}
        Segment subtitles: {segment.subtitles}

        The subtitles can be auto-generated, so don't assume what's written there is the absolute truth, especially the spelling. Double check the information there using the other fields.

        Given this information, could you give me information about the sponsor? I want you to return a json with the following information:

        sponsor_name: Sponsor's name
        sponsor_description: Sponsor's products and services
        sponsor_offer: The specific discount or promo provided by the sponsor, if any
        sponsor_links: List of hyperlinks related to the sponsor, such as affiliate links, homepages, or links to the offer, if any. Make sure these start with http or https
        sponsor_coupon_code: Coupon code, if any

        Please respond with the json enclosed in a ```json ``` markdown code block.
    """
    return prompt


async def create_sponsorships(
    sponsored_segments: list[SponsoredSegment],
    metadata: dict,
    sponsorship_repo: SponsorshipRepository,
    generated_sponsorship_repo: GeneratedSponsorshipRepository,
    session: AsyncSession,
) -> list[Sponsorship]:
    sponsorships = []
    generator = get_generator()
    for sponsored_segment in sponsored_segments:
        prompt = await create_prompt(metadata, sponsored_segment)
        sponsorship = await generator.extract_sponsor_info(prompt)
        sponsorship_create = SponsorshipCreate(
            sponsor_name=sponsorship["sponsor_name"],
            sponsor_description=sponsorship["sponsor_description"],
            sponsor_links=sponsorship["sponsor_links"],
            sponsor_coupon_code=sponsorship["sponsor_coupon_code"],
            sponsor_offer=sponsorship["sponsor_offer"],
            sponsored_segment_id=sponsored_segment.id,
        )
        sponsorship = await sponsorship_repo.add(sponsorship_create, session)
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
        await generated_sponsorship_repo.add(generated_sponsorship_create, session)
        sponsorships.append(sponsorship)
    return sponsorships
