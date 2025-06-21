from backend.schemas.video import VideoUpdate, VideoCreate
from datetime import datetime
from backend.schemas.video_metadata import VideoMetadataCreate, VideoMetadataUpdate
from backend.schemas.sponsored_segment import SponsoredSegmentUpdate, SponsoredSegmentCreate
import pandas as pd
from backend.schemas.sponsorship import SponsorshipCreate
from backend.core.settings import generator_settings
from backend.schemas.video_sponsorship import VideoSponsorshipResponse


class VideoSponsorshipMapper:
    async def map_key_metadata_to_video(self, metadata: dict) -> VideoUpdate:
        return VideoUpdate(
            language=metadata["language"],
            title=metadata["title"],
            upload_date=datetime.strptime(metadata["upload_date"], "%Y%m%d"),
            description=metadata["description"],
            duration=metadata["duration"],
            channel=metadata["channel"],
        )

    async def map_language_metadata_to_video(self, language: str) -> VideoUpdate:
        return VideoUpdate(
            language=language,
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

    async def map_metadata_to_prompt(self, video, segment):
        prompt = f"""
            I have a sponsored segment cut from a Youtube video. Here's some information about this segment:

            Youtube channel: {video.channel}
            Video description: {video.description}
            Upload date: {video.upload_date}
            Video language: {video.language}
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

    async def map_transcript_to_segment_subtitles(self, transcript: str, segment):
        df = pd.DataFrame(transcript)
        start_row = df[df["start"] <= segment.start_time].iloc[-1]
        max_start_time = df["start"].max()
        if segment.end_time <= max_start_time:
            end_row = df[df["start"] >= segment.end_time].iloc[0]
        else:
            end_row = df.iloc[-1]
        df = df.iloc[start_row.name : end_row.name]
        text = " ".join(df["text"].tolist())
        return text

    async def map_sponsorship_data_to_sponsorship(self, sponsorship: dict, segment_id: str):
        return SponsorshipCreate(
            sponsor_name=sponsorship["sponsor_name"],
            sponsor_description=sponsorship["sponsor_description"],
            sponsor_links=sponsorship["sponsor_links"],
            sponsor_coupon_code=sponsorship["sponsor_coupon_code"],
            sponsor_offer=sponsorship["sponsor_offer"],
            sponsored_segment_id=segment_id,
            generator=generator_settings.GENERATOR,
            provider=generator_settings.PROVIDER,
            model=generator_settings.MODEL,
        )

    async def map_entities_to_response(self, sponsorship, segment, video):
        return VideoSponsorshipResponse(
            id=sponsorship.id,
            youtube_id=video.youtube_id,
            start_time=segment.start_time,
            end_time=segment.end_time,
            sponsor_name=sponsorship.sponsor_name,
            sponsor_description=sponsorship.sponsor_description,
            sponsor_links=sponsorship.sponsor_links,
            sponsor_coupon_code=sponsorship.sponsor_coupon_code,
            sponsor_offer=sponsorship.sponsor_offer,
        )
