from backend.schemas.video_sponsorship import VideoSponsorshipRequest
import pytest
from pydantic import ValidationError


@pytest.mark.parametrize(
    "url, expected_output, expected_error",
    [
        (
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            None,
        ),
        ("https://youtu.be/dQw4w9WgXcQ", "https://youtu.be/dQw4w9WgXcQ", None),
        (
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
            None,
        ),
        (
            "https://music.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://music.youtube.com/watch?v=dQw4w9WgXcQ",
            None,
        ),
        ("http://youtube.com/watch?v=dQw4w9WgXcQ", "http://youtube.com/watch?v=dQw4w9WgXcQ", None),
        ("https://www.notyoutube.com/watch?v=dQw4w9WgXcQ", None, ValidationError),
        ("https://youtube.com.evil.com/watch?v=dQw4w9WgXcQ", None, ValidationError),
        ("https://vimeo.com/123456", None, ValidationError),
        ("https://www.youtu.be.com/watch?v=dQw4w9WgXcQ", None, ValidationError),
        ("just some random text", None, ValidationError),
        ("", None, ValidationError),
        (None, None, None),
        ("https://youtu.be.com", None, ValidationError),
        (
            "https://www.YOUTUBE.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            None,
        ),
    ],
)
async def test_validate_youtube_url(url, expected_output, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            VideoSponsorshipRequest(url=url)
    else:
        if not url:
            video = VideoSponsorshipRequest(id="0", url=url)
            assert video.url == expected_output
        else:
            video = VideoSponsorshipRequest(url=url)
            assert str(video.url) == expected_output
