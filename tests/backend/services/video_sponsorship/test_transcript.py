from backend.services.video_sponsorship.transcript import fetch_transcript_and_language
from backend.schemas.video_metadata import TranscriptSegment
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
    print("started test")
    transcript, transcript_language = await fetch_transcript_and_language(
        youtube_id=youtube_id, language=input_language
    )
    assert transcript_language == output_language
    ta_json = TypeAdapter(TranscriptSegment)
    assert isinstance(transcript, list) and all(
        ta_json.validate_python(item) for item in transcript
    )
