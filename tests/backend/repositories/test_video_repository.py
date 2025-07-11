from backend.repositories.all import VideoRepository
from backend.schemas.all import VideoCreate, VideoUpdate
from backend.models.all import Video
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime


@pytest.fixture
def repo():
    return VideoRepository()


@pytest.fixture
def entity_fields():
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
async def test_add_duplicate(test_session, repo, base_fields, entity_fields):
    youtube_id = "IInciWyU74U"

    existing = await repo.get_by_youtube_id(youtube_id, test_session)
    assert not existing

    video_data = {
        "youtube_id": youtube_id,
    }
    video_create = VideoCreate(**video_data)
    video = await repo.add(video_create, test_session)
    for field in base_fields + entity_fields:
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
async def test_add_full(test_session, repo, base_fields, entity_fields):
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
    for field in base_fields + entity_fields:
        assert hasattr(video, field)
    for field in base_fields:
        assert getattr(video, field) is not None
    for k, v in video_data.items():
        if k == "upload_date":
            assert getattr(video, k) == datetime.strptime(v, "%Y-%m-%d").date()
        else:
            assert getattr(video, k) == v


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id(test_session, repo):
    video = await repo.get_by_id("2df9f22f-a2e1-4498-940e-41c105a05f41", test_session)
    assert video is None

    video = await repo.get_by_youtube_id("non-existent", test_session)
    assert video is None

    youtube_id = "On2V_L9jwS4"
    video_data = {"youtube_id": youtube_id}
    video_create = VideoCreate(**video_data)
    video = await repo.add(video_create, test_session)
    id = video.id

    video = await repo.get_by_youtube_id(youtube_id, test_session)
    assert isinstance(video, Video)
    assert video.youtube_id == youtube_id

    video = await repo.get_by_id(id, test_session)
    assert isinstance(video, Video)
    assert video.id == id


@pytest.mark.asyncio(loop_scope="session")
async def test_update(test_session, repo, base_fields, entity_fields):
    retained_fields = ["id", "youtube_id", "created_at"]
    all_fields = base_fields + entity_fields
    changed_fields = [field for field in all_fields if field not in retained_fields]

    id = "a6945747-6dab-429e-a2cf-4c3d2f0e0727"
    await repo.update(id, VideoUpdate(language="en"), test_session)
    updated_video = await repo.get_by_id(id, test_session)
    assert updated_video is None

    original_video_data = {
        "youtube_id": "wyo1u9WxUG4",
        "language": "en",
        "title": "test title",
        "upload_date": "2025-06-24",
        "description": "test description",
        "duration": 12,
        "channel": "another_channel",
    }
    video_create = VideoCreate(**original_video_data)
    added_video = await repo.add(video_create, test_session)
    added_video_data = {k: v for k, v in added_video.__dict__.items() if k in all_fields}
    added_video_copy = Video(**added_video_data)

    new_video_data = {
        "language": "dc",
        "title": "new title",
        "upload_date": "2025-06-26",
        "description": "test description updated",
        "duration": 16,
        "channel": "more_channel",
    }
    video_update = VideoUpdate(**new_video_data)
    await repo.update(added_video.id, video_update, test_session)

    updated_video = await repo.get_by_id(added_video.id, test_session)
    await test_session.refresh(updated_video)
    assert isinstance(updated_video, Video)

    for field in retained_fields:
        assert getattr(added_video, field) == getattr(updated_video, field)
        assert getattr(added_video_copy, field) == getattr(updated_video, field)
    for field in changed_fields:
        assert getattr(added_video, field) == getattr(updated_video, field)
        assert getattr(added_video_copy, field) != getattr(updated_video, field)
        if field == "upload_date":
            assert (
                getattr(updated_video, field)
                == datetime.strptime(new_video_data[field], "%Y-%m-%d").date()
            )
        elif field != "updated_at":
            assert getattr(updated_video, field) == new_video_data[field]
