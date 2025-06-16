from backend.schemas.sponsored_segment import SponsoredSegmentUpdateSubtitles


async def map_segment_subtitles(subtitles: str) -> SponsoredSegmentUpdateSubtitles:
    return SponsoredSegmentUpdateSubtitles(subtitles=subtitles)
