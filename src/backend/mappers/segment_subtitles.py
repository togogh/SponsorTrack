from backend.schemas.sponsored_segment import SponsoredSegmentUpdate


async def map_segment_subtitles(subtitles: str) -> SponsoredSegmentUpdate:
    return SponsoredSegmentUpdate(subtitles=subtitles)
