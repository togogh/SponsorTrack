from backend.repositories.all import VideoMetadataRepository, VideoRepository
from backend.schemas.all import VideoMetadataCreate, VideoMetadataUpdate, VideoCreate
from backend.models.all import VideoMetadata
import pytest
from sqlalchemy.exc import IntegrityError
import datetime


@pytest.fixture
def video_repo():
    return VideoRepository()


@pytest.fixture
def metadata_repo():
    return VideoMetadataRepository()


@pytest.fixture
def entity_fields():
    return list(VideoMetadataCreate.__pydantic_fields__.keys())


@pytest.mark.asyncio(loop_scope="session")
async def test_add(test_session, video_repo, metadata_repo, base_fields, entity_fields):
    youtube_id = "kqeRt2lutI4"

    video_data = {
        "youtube_id": youtube_id,
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    metadata_data = {
        "video_id": video.id,
        "raw_json": {
            "language": "en",
            "title": "title",
            "upload_date": "2024-02-14",
            "description": "description",
            "duration": 92.1,
            "channel": "channel",
        },
    }

    metadata_create = VideoMetadataCreate(**metadata_data)
    metadata = await metadata_repo.add(metadata_create, test_session)
    for field in base_fields + entity_fields:
        assert hasattr(metadata, field)
    for field in base_fields:
        assert getattr(metadata, field) is not None
    for k, v in metadata_data.items():
        assert getattr(metadata, k) == v

    with pytest.raises(IntegrityError):
        try:
            await metadata_repo.add(metadata_create, test_session)
        finally:
            await test_session.rollback()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id(test_session, metadata_repo, video_repo):
    rand_uuid = "2df9f22f-a2e1-4498-940e-41c105a05f41"

    metadata = await metadata_repo.get_by_id(rand_uuid, test_session)
    assert metadata is None

    metadata = await metadata_repo.get_by_video_id(rand_uuid, test_session)
    assert metadata is None

    youtube_id = "wAnDWfEIwoE"
    video_data = VideoCreate(youtube_id=youtube_id)
    video = await video_repo.add(video_data, test_session)

    metadata_data = {
        "video_id": video.id,
        "raw_json": {
            "language": "fr",
            "title": "title",
            "upload_date": "2024-12-14",
            "description": "asdfsdfsd",
            "duration": 37.2,
            "channel": "another channel",
        },
    }
    metadata_create = VideoMetadataCreate(**metadata_data)
    metadata = await metadata_repo.add(metadata_create, test_session)

    queried_metadata = await metadata_repo.get_by_id(metadata.id, test_session)
    assert isinstance(queried_metadata, VideoMetadata)
    assert metadata == queried_metadata

    queried_metadata = await metadata_repo.get_by_video_id(video.id, test_session)
    assert isinstance(queried_metadata, VideoMetadata)
    assert metadata == queried_metadata


@pytest.mark.asyncio(loop_scope="session")
async def test_update(test_session, video_repo, metadata_repo, base_fields, entity_fields):
    retained_fields = ["id", "video_id", "created_at"]
    all_fields = base_fields + entity_fields
    changed_fields = [field for field in all_fields if field not in retained_fields]

    id = "a6945747-6dab-429e-a2cf-4c3d2f0e0727"
    await metadata_repo.update(
        id,
        VideoMetadataUpdate(
            raw_json={
                "language": "fr",
                "title": "title",
                "upload_date": "2024-12-14",
                "description": "asdfsdfsd",
                "duration": 37.2,
                "channel": "another channel",
            }
        ),
        test_session,
    )
    updated_metdata = await metadata_repo.get_by_id(id, test_session)
    assert updated_metdata is None

    video_data = {
        "youtube_id": "vDWaKVmqznQ",
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    original_metadata_data = {
        "video_id": video.id,
        "raw_json": {
            "language": "en-us",
            "title": "title",
            "upload_date": "2023-12-14",
            "description": "desc",
            "duration": 182.2,
            "channel": "chann",
        },
    }
    metadata_create = VideoMetadataCreate(**original_metadata_data)
    added_metadata = await metadata_repo.add(metadata_create, test_session)
    added_metadata_data = {k: v for k, v in added_metadata.__dict__.items() if k in all_fields}
    added_metadata_copy = VideoMetadata(**added_metadata_data)

    new_metadata_data = {
        "raw_json": {
            "language": "pso",
            "title": "another title",
            "upload_date": "2023-12-20",
            "description": "description",
            "duration": 182.5,
            "channel": "channel",
        },
        "raw_transcript": [{"text": "subtitles", "start": 2.4, "duration": 12}],
    }
    metadata_update = VideoMetadataUpdate(**new_metadata_data)
    await metadata_repo.update(added_metadata.id, metadata_update, test_session)

    updated_metadata = await metadata_repo.get_by_id(added_metadata.id, test_session)
    await test_session.refresh(updated_metadata)
    assert isinstance(updated_metadata, VideoMetadata)

    for field in retained_fields:
        assert getattr(added_metadata, field) == getattr(updated_metadata, field)
        assert getattr(added_metadata_copy, field) == getattr(updated_metadata, field)
    for field in changed_fields:
        assert getattr(added_metadata, field) == getattr(updated_metadata, field)
        assert getattr(added_metadata_copy, field) != getattr(updated_metadata, field)
        if field == "upload_date":
            assert (
                getattr(updated_metadata, field)
                == datetime.strptime(new_metadata_data[field], "%Y-%m-%d").date()
            )
        elif field != "updated_at":
            assert getattr(updated_metadata, field) == new_metadata_data[field]
