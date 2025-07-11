from backend.repositories.all import SponsoredSegmentRepository, VideoRepository
from backend.schemas.all import SponsoredSegmentCreate, SponsoredSegmentUpdate, VideoCreate  # noqa: F401
from backend.models.all import SponsoredSegment  # noqa: F401
import pytest
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def video_repo():
    return VideoRepository()


@pytest.fixture
def sponsored_segment_repo():
    return SponsoredSegmentRepository()


@pytest.fixture
def entity_fields():
    return [
        "sponsorblock_id",
        "start_time",
        "end_time",
        "parent_video_id",
        "subtitles",
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_add_overlapping(
    test_session, sponsored_segment_repo, video_repo, base_fields, entity_fields
):
    youtube_id = "CvQ7e6yUtnw"
    video_data = {
        "youtube_id": youtube_id,
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)
    video_id = video.id

    first_segment_data = {
        "sponsorblock_id": "id1",
        "start_time": 10,
        "end_time": 15,
        "parent_video_id": video_id,
    }
    sponsored_segment_create = SponsoredSegmentCreate(**first_segment_data)
    sponsored_segment = await sponsored_segment_repo.add(sponsored_segment_create, test_session)
    for field in base_fields + entity_fields:
        assert hasattr(sponsored_segment, field)
    for field in base_fields:
        assert getattr(sponsored_segment, field) is not None
    for k, v in first_segment_data.items():
        assert getattr(sponsored_segment, k) == v

    second_segment_data = {
        "sponsorblock_id": "id1",
        "start_time": 18,
        "end_time": 25,
        "parent_video_id": video_id,
    }
    sponsored_segment_create = SponsoredSegmentCreate(**second_segment_data)
    with pytest.raises(IntegrityError):
        try:
            await sponsored_segment_repo.add(sponsored_segment_create, test_session)
        finally:
            await test_session.rollback()

    print("this is the video", video)
    print(video_id)
    third_segment_data = {
        "sponsorblock_id": "id2",
        "start_time": 12,
        "end_time": 25,
        "parent_video_id": video_id,
    }
    sponsored_segment_create = SponsoredSegmentCreate(**third_segment_data)
    with pytest.raises(IntegrityError):
        try:
            await sponsored_segment_repo.add(sponsored_segment_create, test_session)
        finally:
            await test_session.rollback()
