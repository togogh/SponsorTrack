from backend.services.video_sponsorship.transcript import (
    fetch_transcript_and_language,
    map_transcript_to_segment_subtitles,
)
from backend.schemas.video_metadata import TranscriptSegment
from backend.models.all import SponsoredSegment
import pytest
from pydantic import TypeAdapter


@pytest.mark.parametrize(
    "youtube_id, input_language, output_language",
    [
        ("l6rRz7sr2Nw", None, "en"),
        ("1E3JfM_6LF4", "en", "en"),
        ("1E3JfM_6LF4", "ja", "ja"),
    ],
)
async def test_fetch_transcript_and_language(youtube_id, input_language, output_language):
    transcript, transcript_language = await fetch_transcript_and_language(
        youtube_id=youtube_id, language=input_language
    )
    assert transcript_language == output_language
    ta_json = TypeAdapter(TranscriptSegment)
    assert isinstance(transcript, list) and all(
        ta_json.validate_python(item) for item in transcript
    )


@pytest.mark.parametrize(
    "transcript, segment_dict, expected_subtitles",
    [
        (
            [
                {"text": "Welcome back to the channel.", "start": 2.0, "duration": 2.5},
                {
                    "text": "Today we'll dive into data visualization.",
                    "start": 4.5,
                    "duration": 3.0,
                },
                {"text": "Let’s look at some examples.", "start": 7.5, "duration": 1.8},
            ],
            {
                "start_time": 0,
                "end_time": 5.5,
                "parent_video_id": "50e62675-875d-4f89-b1de-875aacac6b9c",
            },
            "Welcome back to the channel. Today we'll dive into data visualization.",
        ),
        (
            [
                {"text": "Let’s start with a bit of history.", "start": 0.0, "duration": 2.4},
                {"text": "The origins go back several centuries.", "start": 2.5, "duration": 2.5},
                {
                    "text": "It wasn’t until the 20th century that we saw real growth.",
                    "start": 5.1,
                    "duration": 3.2,
                },
            ],
            {
                "start_time": 2,
                "end_time": 5,
                "parent_video_id": "50e62675-875d-4f89-b1de-875aacac6b9c",
            },
            "Let’s start with a bit of history. The origins go back several centuries.",
        ),
        (
            [
                {"text": "Uh, so I think it started around noon.", "start": 5.0, "duration": 2.0},
                {
                    "text": "We were just hanging out, nothing unusual.",
                    "start": 7.2,
                    "duration": 2.3,
                },
                {"text": "Then suddenly there was a loud bang.", "start": 9.5, "duration": 1.7},
            ],
            {
                "start_time": 7,
                "end_time": 15,
                "parent_video_id": "50e62675-875d-4f89-b1de-875aacac6b9c",
            },
            "Uh, so I think it started around noon. We were just hanging out, nothing unusual. Then suddenly there was a loud bang.",
        ),
    ],
)
async def test_map_transcript_to_segment_subtitles(transcript, segment_dict, expected_subtitles):
    segment = SponsoredSegment(**segment_dict)
    subtitles = await map_transcript_to_segment_subtitles(transcript, segment)
    assert subtitles == expected_subtitles
