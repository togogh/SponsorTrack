from backend.repositories.all import VideoRepository
from backend.schemas.all import VideoCreate
import pytest
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def repo():
    return VideoRepository()


@pytest.fixture
def video_fields():
    return [
        "youtube_id",
        "language",
        "title",
        "upload_date",
        "description",
        "duration",
        "channel",
    ]


async def test_add(test_session, repo, base_fields, video_fields):
    youtube_id = "IInciWyU74U"
    existing = await repo.get_by_youtube_id(youtube_id, test_session)
    assert not existing
    video_data = VideoCreate(youtube_id=youtube_id)
    video = await repo.add(video_data, test_session)
    for field in base_fields + video_fields:
        assert hasattr(video, field)
    for field in base_fields:
        assert getattr(video, field) is not None
    assert video.youtube_id == youtube_id
    with pytest.raises(IntegrityError):
        await repo.add(video_data, test_session)
