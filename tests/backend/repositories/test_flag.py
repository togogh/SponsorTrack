from backend.repositories.all import (
    SponsoredSegmentRepository,
    VideoRepository,
    SponsorshipRepository,
    FlagRepository,
)
from backend.schemas.all import (
    SponsoredSegmentCreate,
    VideoCreate,
    SponsorshipCreate,
    FlagCreate,
    FlagUpdate,
    SponsoredSegmentFlagCreate,
    SponsorshipFlagCreate,
    VideoFlagCreate,
)
from backend.schemas.flag import FlagStatus
from backend.models.flag import EntityType
from backend.models.all import Flag
import pytest


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
def flag_repo():
    return FlagRepository()


@pytest.fixture
def entity_fields():
    return list(FlagCreate.__pydantic_fields__.keys())


@pytest.mark.asyncio(loop_scope="session")
async def test_add(test_session, video_repo, flag_repo, base_fields, entity_fields):
    youtube_id = "jfWa-GD0szU"
    video_data = {
        "youtube_id": youtube_id,
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    video_flag_data = {
        "field_flagged": "num_sponsored_segments",
        "value_flagged": 0,
        "entity_id": video.id,
    }
    video_flag_create = VideoFlagCreate(**video_flag_data)
    flag = await flag_repo.add(EntityType.video, video_flag_create, test_session)
    for field in base_fields + entity_fields:
        assert hasattr(flag, field)
    for field in base_fields:
        assert getattr(flag, field) is not None
    for k, v in video_flag_data.items():
        assert getattr(flag, k) == v


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id(
    test_session, sponsored_segment_repo, video_repo, sponsorship_repo, flag_repo
):
    youtube_id = "c5Kdv1t0NsE"
    video_data = {
        "youtube_id": youtube_id,
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    segment_data = {
        "start_time": 35,
        "end_time": 76,
        "parent_video_id": video.id,
    }
    sponsored_segment_create = SponsoredSegmentCreate(**segment_data)
    sponsored_segment = await sponsored_segment_repo.add(sponsored_segment_create, test_session)

    sponsor_data = {"sponsor_name": "Sponsor", "sponsored_segment_id": sponsored_segment.id}
    sponsorship_create = SponsorshipCreate(**sponsor_data)
    sponsorship = await sponsorship_repo.add(sponsorship_create, test_session)

    video_flag_data = {
        "field_flagged": "num_sponsored_segments",
        "value_flagged": 0,
        "entity_id": video.id,
    }
    video_flag_create = VideoFlagCreate(**video_flag_data)
    flag = await flag_repo.add(EntityType.video, video_flag_create, test_session)

    queried_flags = await flag_repo.get_by_video_id(video.id, test_session)
    queried_flag = queried_flags[0]
    assert isinstance(queried_flag, Flag)
    assert flag == queried_flag

    segment_flag_data = {
        "field_flagged": "subtitles",
        "value_flagged": "blabla",
        "entity_id": sponsored_segment.id,
    }
    segment_flag_create = SponsoredSegmentFlagCreate(**segment_flag_data)
    flag = await flag_repo.add(EntityType.sponsored_segment, segment_flag_create, test_session)

    queried_flags = await flag_repo.get_by_segment_id(sponsored_segment.id, test_session)
    queried_flag = queried_flags[0]
    assert isinstance(queried_flag, Flag)
    assert flag == queried_flag

    sponsorship_flag_data = {
        "field_flagged": "sponsor_name",
        "value_flagged": 0,
        "entity_id": sponsorship.id,
    }
    sponsorship_flag_create = SponsorshipFlagCreate(**sponsorship_flag_data)
    flag = await flag_repo.add(EntityType.sponsorship, sponsorship_flag_create, test_session)

    queried_flags = await flag_repo.get_by_sponsorship_id(sponsorship.id, test_session)
    queried_flag = queried_flags[0]
    assert isinstance(queried_flag, Flag)
    assert flag == queried_flag

    queried_flag = await flag_repo.get_by_id(flag.id, test_session)
    assert isinstance(queried_flag, Flag)
    assert flag == queried_flag


@pytest.mark.asyncio(loop_scope="session")
async def test_update(test_session, video_repo, flag_repo, base_fields, entity_fields):
    retained_fields = ["id", "entity_id", "created_at", "field_flagged", "value_flagged"]
    all_fields = base_fields + entity_fields
    changed_fields = [field for field in all_fields if field not in retained_fields]

    youtube_id = "r9UliCVsDcw"
    video_data = {
        "youtube_id": youtube_id,
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    video_flag_data = {
        "field_flagged": "title",
        "value_flagged": video.title,
        "entity_id": video.id,
    }
    video_flag_create = VideoFlagCreate(**video_flag_data)
    added_flag = await flag_repo.add(EntityType.video, video_flag_create, test_session)
    added_flag_data = {k: v for k, v in added_flag.__dict__.items() if k in all_fields}
    added_flag_copy = Flag(**added_flag_data)

    new_video_flag_data = {
        "status": FlagStatus.resolved,
    }
    video_flag_update = FlagUpdate(**new_video_flag_data)
    await flag_repo.update(added_flag.id, video_flag_update, test_session)

    updated_flag = await flag_repo.get_by_id(added_flag.id, test_session)
    await test_session.refresh(updated_flag)
    assert isinstance(updated_flag, Flag)

    for field in retained_fields:
        assert getattr(added_flag, field) == getattr(updated_flag, field)
        assert getattr(added_flag_copy, field) == getattr(updated_flag, field)
    for field in changed_fields:
        assert getattr(added_flag, field) == getattr(updated_flag, field)
        assert getattr(added_flag_copy, field) != getattr(updated_flag, field)
        if field != "updated_at":
            assert getattr(updated_flag, field) == new_video_flag_data[field]
