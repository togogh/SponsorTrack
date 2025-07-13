from backend.schemas.video_metadata import VideoMetadataUpdate
import pytest
from pydantic import ValidationError


@pytest.mark.parametrize(
    "raw_json, expected_error",
    [
        (
            {
                "language": "en",
                "title": "title",
                "upload_date": "2024-02-14",
                "description": "description",
                "duration": 92.1,
                "channel": "channel",
            },
            None,
        ),
        (
            {
                "language": "en",
                "title": "title",
                "upload_date": "2024-02-14",
                "description": "description",
                "duration": 92.1,
                "channel": "channel",
                "extra_field": "extra",
            },
            None,
        ),
        ({"extra_field": "extra"}, ValidationError),
        (
            {
                "language": "en",
                "title": "title",
                "upload_date": "2024-22-14",
                "description": "description",
                "duration": 92.1,
                "channel": "channel",
            },
            ValidationError,
        ),
    ],
)
async def test_raw_json(raw_json, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            VideoMetadataUpdate(raw_json=raw_json)
    else:
        sponsorship = VideoMetadataUpdate(raw_json=raw_json)
        assert sponsorship.raw_json == raw_json


@pytest.mark.parametrize(
    "raw_transcript, expected_error",
    [
        (["subtitles"], ValidationError),
        ("subtitles", ValidationError),
        (
            [
                {
                    "text": "subtitles",
                    "start": 125,
                    "duration": 29,
                },
                {
                    "text": "more subtitles",
                    "start": 169,
                    "duration": 80,
                },
            ],
            None,
        ),
        (
            [
                {
                    "text": "subtitles",
                    "start": 125,
                },
                {
                    "text": "more subtitles",
                    "start": 169,
                    "duration": 80,
                },
            ],
            ValidationError,
        ),
    ],
)
async def test_raw_transcript(raw_transcript, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            VideoMetadataUpdate(raw_transcript=raw_transcript)
    else:
        sponsorship = VideoMetadataUpdate(raw_transcript=raw_transcript)
        assert sponsorship.raw_transcript == raw_transcript
