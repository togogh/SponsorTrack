from backend.schemas.flag import VideoFlagPostParams
import pytest
from pydantic import ValidationError


@pytest.mark.parametrize(
    "youtube_id, video_id, expected_error",
    [
        pytest.param("7a_wOgXrHn8", "b23cf2b9-e5da-42ed-b1d1-0ef7c5974b01", ValidationError),
        pytest.param(None, "b23cf2b9-e5da-42ed-b1d1-0ef7c5974b01", None),
        pytest.param(None, "invalid-id", ValidationError),
        pytest.param("7a_wOgXrHn8", None, None),
        pytest.param(None, None, ValidationError),
    ],
)
async def test_ensure_one_id(youtube_id, video_id, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            VideoFlagPostParams(youtube_id=youtube_id, video_id=video_id)
    else:
        params = VideoFlagPostParams(youtube_id=youtube_id, video_id=video_id)
        assert params.youtube_id == youtube_id
        assert str(params.video_id) == str(video_id)
