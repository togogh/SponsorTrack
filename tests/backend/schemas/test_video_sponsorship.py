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
            request = VideoSponsorshipRequest(id="0", url=url)
            assert request.url == expected_output
        else:
            request = VideoSponsorshipRequest(url=url)
            assert str(request.url) == expected_output


@pytest.mark.parametrize(
    "input, expected_error",
    [
        (
            {"id": "dQw4w9WgXcQ", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            ValidationError,
        ),
        ({"id": None, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}, None),
        ({"id": "dQw4w9WgXcQ", "url": None}, None),
        ({"id": None, "url": None}, ValidationError),
    ],
)
async def test_ensure_url_or_id(input, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            VideoSponsorshipRequest(**input)
    else:
        request = VideoSponsorshipRequest(**input)
        for k, v in input.items():
            if v is None:
                assert getattr(request, k) == v
            else:
                assert str(getattr(request, k)) == v
