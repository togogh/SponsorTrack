from backend.services.video_sponsorship.sponsored_segments import (
    download_sponsorblock,
    get_sponsored_segments,  # noqa: F401
    get_or_create_sponsored_segments,  # noqa: F401
)
import pytest
from fastapi.exceptions import HTTPException


@pytest.mark.parametrize(
    "youtube_id, len_blocks, error",
    [
        ("1-_AhiAPyZg", 0, HTTPException),
        ("BsBSgtkmjak", 2, None),
    ],
)
async def test_download_sponsorblock(youtube_id, len_blocks, error):
    if error is not None:
        with pytest.raises(error):
            await download_sponsorblock(youtube_id)
    else:
        blocks = await download_sponsorblock(youtube_id)
        assert len(blocks) == len_blocks
