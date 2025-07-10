from backend.repositories.all import VideoRepository
from backend.schemas.all import VideoCreate
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime


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


@pytest.mark.asyncio(loop_scope="session")
async def test_add_duplicate(test_session, repo, base_fields, video_fields):
    youtube_id = "IInciWyU74U"

    existing = await repo.get_by_youtube_id(youtube_id, test_session)
    assert not existing

    video_data = {
        "youtube_id": youtube_id,
    }
    video_create = VideoCreate(**video_data)
    video = await repo.add(video_create, test_session)
    for field in base_fields + video_fields:
        assert hasattr(video, field)
    for field in base_fields:
        assert getattr(video, field) is not None
    for k, v in video_data.items():
        assert getattr(video, k) == v

    with pytest.raises(IntegrityError):
        try:
            await repo.add(video_create, test_session)
        finally:
            await test_session.rollback()


@pytest.mark.asyncio(loop_scope="session")
async def test_add_full(test_session, repo, base_fields, video_fields):
    video_data = {
        "youtube_id": "VWUXDDM_TAQ",
        "language": "en",
        "title": "test title",
        "upload_date": "2025-03-24",
        "description": "test description",
        "duration": 15,
        "channel": "test_channel",
    }
    video_create = VideoCreate(**video_data)
    video = await repo.add(video_create, test_session)
    for field in base_fields + video_fields:
        assert hasattr(video, field)
    for field in base_fields:
        assert getattr(video, field) is not None
    for k, v in video_data.items():
        if k == "upload_date":
            assert getattr(video, k) == datetime.strptime(v, "%Y-%m-%d").date()
        else:
            assert getattr(video, k) == v
