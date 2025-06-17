from backend.schemas.video import VideoUpdate, VideoCreate
from datetime import datetime
from backend.schemas.video_metadata import VideoMetadataCreate, VideoMetadataUpdate
from backend.schemas.sponsored_segment import SponsoredSegmentUpdate, SponsoredSegmentCreate


class VideoSponsorshipMapper:
    async def map_key_metadata_to_video(self, metadata: dict) -> VideoUpdate:
        return VideoUpdate(
            language=metadata["language"],
            title=metadata["title"],
            upload_date=datetime.strptime(metadata["upload_date"], "%Y%m%d"),
            description=metadata["description"],
            duration=metadata["duration"],
        )

    async def map_metadata_json_to_videometadata(
        self, video_id: str, raw_json: dict
    ) -> VideoMetadataCreate:
        return VideoMetadataCreate(
            raw_json=raw_json,
            video_id=video_id,
        )

    async def map_metadata_transcript_to_videometadata(
        self, raw_transcript: list
    ) -> VideoMetadataUpdate:
        return VideoMetadataUpdate(
            raw_transcript=raw_transcript,
        )

    async def map_subtitles_to_sponsoredsegment(self, subtitles: str) -> SponsoredSegmentUpdate:
        return SponsoredSegmentUpdate(subtitles=subtitles)

    async def map_sponsorblock_to_sponsored_segment(
        self, sponsorblock: dict, parent_video_id: str
    ) -> SponsoredSegmentCreate:
        return SponsoredSegmentCreate(
            sponsorblock_id=sponsorblock["UUID"],
            start_time=sponsorblock["segment"][0],
            end_time=sponsorblock["segment"][1],
            duration=sponsorblock["segment"][1] - sponsorblock["segment"][0],
            parent_video_id=parent_video_id,
        )

    async def map_youtube_id_to_video(self, youtube_id: str) -> VideoCreate:
        return VideoCreate(youtube_id=youtube_id)
