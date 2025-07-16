from backend.services.video_sponsorship.video import (
    extract_id_from_url,
    get_youtube_id,
    create_video,
    get_or_create_video,  # noqa: F401
)
import pytest
from fastapi.exceptions import HTTPException
from backend.repositories.all import VideoRepository
from backend.models.all import Video
from pydantic import ValidationError


@pytest.fixture
def repo():
    return VideoRepository()


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


@pytest.mark.parametrize(
    "youtube_id, error",
    [
        ("YDX1-5T_uQ4", None),
        ("A1b2C3d4E5F", ValidationError),
        ("", ValidationError),
        (None, ValidationError),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_create_video(youtube_id, error, repo, test_session):
    if error is not None:
        with pytest.raises(error):
            try:
                await create_video(youtube_id, repo, test_session)
            finally:
                await test_session.rollback()
    else:
        video = await create_video(youtube_id, repo, test_session)
        assert isinstance(video, Video)
        assert video.youtube_id == youtube_id
