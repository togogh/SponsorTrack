from backend.repositories.all import (
    SponsoredSegmentRepository,
    VideoRepository,
    SponsorshipRepository,
)
from backend.schemas.all import (
    SponsoredSegmentCreate,
    SponsoredSegmentUpdate,
    VideoCreate,
    SponsorshipCreate,
)
from backend.models.all import SponsoredSegment
import pytest
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def video_repo():
    return VideoRepository()


@pytest.fixture
def sponsored_segment_repo():
    return SponsoredSegmentRepository()


@pytest.fixture
def sponsorship_repo():
    return SponsorshipRepository()


@pytest.fixture
def entity_fields():
    return list(SponsoredSegmentCreate.__pydantic_fields__.keys())


@pytest.mark.asyncio(loop_scope="session")
async def test_add(test_session, sponsored_segment_repo, video_repo, base_fields, entity_fields):
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


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id(test_session, sponsored_segment_repo, video_repo, sponsorship_repo):
    rand_uuid = "2df9f22f-a2e1-4498-940e-41c105a05f41"

    segment = await sponsored_segment_repo.get_by_id(rand_uuid, test_session)
    assert segment is None

    segment = await sponsored_segment_repo.get_by_sponsorblock_id(rand_uuid, test_session)
    assert segment is None

    segment = await sponsored_segment_repo.get_by_sponsorship_id(rand_uuid, test_session)
    assert segment is None

    segments = await sponsored_segment_repo.get_by_video_id(rand_uuid, test_session)
    assert segments == []

    youtube_id = "sR7rMP4GXuE"
    video_data = VideoCreate(youtube_id=youtube_id)
    video = await video_repo.add(video_data, test_session)

    segment_data = [
        {
            "sponsorblock_id": "sblock_1",
            "start_time": 1,
            "end_time": 5,
            "parent_video_id": video.id,
        },
        {
            "sponsorblock_id": "sblock_2",
            "start_time": 13.1,
            "end_time": 119.2,
            "parent_video_id": video.id,
        },
    ]
    segments = []
    for data in segment_data:
        segment_create = SponsoredSegmentCreate(**data)
        segment = await sponsored_segment_repo.add(segment_create, test_session)
        segments.append(segment)

    sponsorship_data = {
        "sponsor_name": "Sponsor",
        "sponsor_description": "we awesome",
        "sponsored_segment_id": segments[0].id,
    }
    sponsorship_create = SponsorshipCreate(**sponsorship_data)
    sponsorship = await sponsorship_repo.add(sponsorship_create, test_session)

    for segment in segments:
        queried_segment = await sponsored_segment_repo.get_by_id(segment.id, test_session)
        assert isinstance(queried_segment, SponsoredSegment)
        assert segment == queried_segment

        queried_segment = await sponsored_segment_repo.get_by_sponsorblock_id(
            segment.sponsorblock_id, test_session
        )
        assert isinstance(queried_segment, SponsoredSegment)
        assert segment == queried_segment

    queried_segment = await sponsored_segment_repo.get_by_sponsorship_id(
        sponsorship.id, test_session
    )
    assert isinstance(queried_segment, SponsoredSegment)
    assert segments[0] == queried_segment

    queried_segments = await sponsored_segment_repo.get_by_video_id(video.id, test_session)
    assert isinstance(queried_segments, list) and all(
        isinstance(item, SponsoredSegment) for item in queried_segments
    )
    assert queried_segments == segments


@pytest.mark.asyncio(loop_scope="session")
async def test_update(test_session, sponsored_segment_repo, video_repo, base_fields, entity_fields):
    retained_fields = ["id", "created_at", "parent_video_id", "sponsorblock_id"]
    all_fields = base_fields + entity_fields
    changed_fields = [field for field in all_fields if field not in retained_fields]

    id = "a6945747-6dab-429e-a2cf-4c3d2f0e0727"
    await sponsored_segment_repo.update(
        id, SponsoredSegmentUpdate(subtitles="blabla"), test_session
    )
    updated_sponsored_segment = await sponsored_segment_repo.get_by_id(id, test_session)
    assert updated_sponsored_segment is None

    video_data = {
        "youtube_id": "e1XgXBsXIRs",
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    original_segment_data = {
        "sponsorblock_id": "rand_id",
        "start_time": 1,
        "end_time": 5,
        "parent_video_id": video.id,
    }
    segment_create = SponsoredSegmentCreate(**original_segment_data)
    added_segment = await sponsored_segment_repo.add(segment_create, test_session)
    added_segment_data = {k: v for k, v in added_segment.__dict__.items() if k in all_fields}
    added_segment_copy = SponsoredSegment(**added_segment_data)

    new_segment_data = {
        "start_time": 10,
        "end_time": 15,
        "subtitles": "bla bla",
    }
    segment_update = SponsoredSegmentUpdate(**new_segment_data)
    await sponsored_segment_repo.update(added_segment.id, segment_update, test_session)

    updated_segment = await sponsored_segment_repo.get_by_id(added_segment.id, test_session)
    await test_session.refresh(updated_segment)
    assert isinstance(updated_segment, SponsoredSegment)

    for field in retained_fields:
        assert getattr(added_segment, field) == getattr(updated_segment, field)
        assert getattr(added_segment_copy, field) == getattr(updated_segment, field)
    for field in changed_fields:
        assert getattr(added_segment, field) == getattr(updated_segment, field)
        assert getattr(added_segment_copy, field) != getattr(updated_segment, field)
        if field != "updated_at":
            assert getattr(updated_segment, field) == new_segment_data[field]
