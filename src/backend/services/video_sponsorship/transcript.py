from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api.formatters import JSONFormatter
import time
import json
from backend.core.settings import ws_settings
from backend.models.all import Video, VideoMetadata, SponsoredSegment
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.all import VideoUpdate, VideoMetadataUpdate, SponsoredSegmentUpdate
import pandas as pd
from backend.repositories.all import (
    VideoMetadataRepository,
    VideoRepository,
    SponsoredSegmentRepository,
)
from backend.logs.config import get_logger

logger = get_logger(__name__)


async def fetch_transcript_and_language(youtube_id, language, retries=5, backoff_factor=0.1):
    if ws_settings.WS_PROXY_UN and ws_settings.WS_PROXY_PW:
        proxy_config = WebshareProxyConfig(
            proxy_username=ws_settings.WS_PROXY_UN,
            proxy_password=ws_settings.WS_PROXY_PW,
        )
        ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
    else:
        ytt_api = YouTubeTranscriptApi()
    for r in range(retries):
        logger.info(
            f"Trying to download transcript for {youtube_id}, current language is {language}."
        )
        try:
            if language is None:
                transcript_list = ytt_api.list(youtube_id)
                language = list(transcript_list)[0].language_code
            transcript = ytt_api.fetch(video_id=youtube_id, languages=[language])
            formatter = JSONFormatter()
            transcript = formatter.format_transcript(transcript, indent=4)
            transcript = json.loads(transcript)
            logger.info("Successfully downloaded transcript.")
            return transcript, language
        except Exception as e:
            logger.error("Encountered error:", e)
            if r < retries:
                print("Retrying...")
                time.sleep(backoff_factor * (2 ** (r - 1)))


async def get_or_fill_transcript(
    video_metadata: VideoMetadata,
    video: Video,
    video_repo: VideoRepository,
    video_metadata_repo: VideoMetadataRepository,
    session: AsyncSession,
) -> dict:
    transcript = video_metadata.raw_transcript
    if transcript is None:
        transcript, transcript_language = await fetch_transcript_and_language(
            video.youtube_id, video.language
        )
        if video.language is None:
            video_update = VideoUpdate(
                language=transcript_language,
            )
            await video_repo.update(video.id, video_update, session)
        video_metadata_update = VideoMetadataUpdate(
            raw_transcript=transcript,
        )
        await video_metadata_repo.update(video_metadata.id, video_metadata_update, session)
    return transcript


async def map_transcript_to_segment_subtitles(transcript: str, segment):
    df = pd.DataFrame(transcript)
    df = df.sort_values(by=["start"], ascending=True)
    if segment.start_time < df.iloc[0]["start"]:
        start_row = df.iloc[0]
    else:
        start_row = df[df["start"] <= segment.start_time].iloc[-1]
    max_start_time = df["start"].max()
    if segment.end_time <= max_start_time:
        end_row = df[df["start"] >= segment.end_time].iloc[0]
    else:
        end_row = df.iloc[-1]
    df = df.iloc[start_row.name : end_row.name]
    text = " ".join(df["text"].tolist())
    return text


async def ensure_subtitles_filled(
    sponsored_segments: list[SponsoredSegment],
    video_metadata: VideoMetadata,
    video: Video,
    sponsored_segment_repo: SponsoredSegmentRepository,
    video_repo: VideoRepository,
    video_metadata_repo: VideoMetadataRepository,
    session: AsyncSession,
) -> list[SponsoredSegment]:
    empty_subtitles_segments = [
        segment.id for segment in sponsored_segments if segment.subtitles is None
    ]
    if len(empty_subtitles_segments) > 0:
        transcript = await get_or_fill_transcript(
            video_metadata, video, video_repo, video_metadata_repo, session
        )
        for segment in sponsored_segments:
            segment.subtitles = await map_transcript_to_segment_subtitles(transcript, segment)
            sponsored_segment_update = SponsoredSegmentUpdate(subtitles=segment.subtitles)
            await sponsored_segment_repo.update(segment.id, sponsored_segment_update, session)
    return sponsored_segments
