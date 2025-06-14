from backend.schemas.sponsored_segment import SponsoredSegmentCreate


async def map_sponsorblock_to_sponsored_segment(
    sponsorblock: dict, parent_video_id: str
) -> SponsoredSegmentCreate:
    return SponsoredSegmentCreate(
        sponsorblock_id=sponsorblock["UUID"],
        start_time=sponsorblock["segment"][0],
        end_time=sponsorblock["segment"][1],
        duration=sponsorblock["segment"][1] - sponsorblock["segment"][0],
        parent_video_id=parent_video_id,
    )
