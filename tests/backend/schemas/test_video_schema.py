from backend.schemas.video import VideoCreate
import pytest


@pytest.mark.parametrize(
    "youtube_id, expected_error",
    [
        pytest.param("7a_wOgXrHn8", None),
        pytest.param("invalid_id", ValueError),
    ],
)
async def test_ensure_video_exists_on_youtube(youtube_id, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            VideoCreate(youtube_id=youtube_id)
    else:
        video = VideoCreate(youtube_id=youtube_id)
        assert video.youtube_id == youtube_id
