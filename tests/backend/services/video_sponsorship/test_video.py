from backend.services.video_sponsorship.video import (
    extract_id_from_url,
    get_youtube_id,  # noqa: F401
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
        url = await extract_id_from_url(input)
        assert url == output
