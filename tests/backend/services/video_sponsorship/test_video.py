from backend.services.video_sponsorship.video import (
    extract_id_from_url,
    get_youtube_id,
    create_video,  # noqa: F401
    get_or_create_video,  # noqa: F401
)
import pytest
from fastapi.exceptions import HTTPException


@pytest.mark.parametrize(
    "input, output, error",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s", "dQw4w9WgXcQ", None),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be", "dQw4w9WgXcQ", None),
        ("https://www.youtube.com/watch?v=", "", HTTPException),
        ("https://www.youtube.com/watch?vid=dQw4w9WgXcQ", "", HTTPException),
        ("https://www.youtube.com/watch", "", HTTPException),
        ("https://www.youtube.com/embed/", "", HTTPException),
        ("https://youtu.be/", "", HTTPException),
        ("https://m.youtube.com/watch", "", HTTPException),
        ("https://m.youtube.com/watch?v=", "", HTTPException),
        (
            "https://www.youtube.com/playlist?list=PL9tY0BWXOZFtcyH4T7pXfKHLGxN1h0DHz",
            "",
            HTTPException,
        ),
        ("https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ", "", HTTPException),
        ("https://www.youtube.com/user/PewDiePie", "", HTTPException),
    ],
)
async def test_extract_id_from_url(input, output, error):
    if error is not None:
        with pytest.raises(error):
            await extract_id_from_url(input)
    else:
        id = await extract_id_from_url(input)
        assert id == output


@pytest.mark.parametrize(
    "id, url, output, error",
    [
        ("dQw4w9WgXcQ", None, "dQw4w9WgXcQ", None),
        (None, "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        (None, "https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        (None, "https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        (None, "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s", "dQw4w9WgXcQ", None),
        (None, "https://m.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        (None, "", None, HTTPException),
        (None, "https://www.youtube.com/watch?v=", None, HTTPException),
        (None, "https://www.youtube.com/watch?vid=dQw4w9WgXcQ", None, HTTPException),
        (None, "https://www.youtube.com/embed/", None, HTTPException),
        (None, "https://youtu.be/", None, HTTPException),
        (None, "https://www.youtube.com/playlist?list=PL123", None, HTTPException),
        (None, "https://www.youtube.com/channel/UC123", None, HTTPException),
        (None, "https://www.youtube.com/user/ExampleUser", None, HTTPException),
    ],
)
async def test_get_youtube_id(id, url, output, error):
    if error is not None:
        with pytest.raises(error):
            await get_youtube_id(id, url)
    else:
        extracted_id = await get_youtube_id(id, url)
        assert extracted_id == output
