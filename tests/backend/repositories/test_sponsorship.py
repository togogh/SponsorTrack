from backend.repositories.all import (
    SponsoredSegmentRepository,
    VideoRepository,
    SponsorshipRepository,
)
from backend.schemas.all import (
    SponsoredSegmentCreate,
    VideoCreate,
    SponsorshipCreate,
    SponsorshipUpdate,
)
from backend.models.all import Sponsorship
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
    return list(SponsorshipCreate.__pydantic_fields__.keys())


@pytest.mark.asyncio(loop_scope="session")
async def test_add(
    test_session, sponsored_segment_repo, video_repo, sponsorship_repo, base_fields, entity_fields
):
    youtube_id = "bnD6bf0K350"
    video_data = {
        "youtube_id": youtube_id,
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    first_segment_data = {
        "start_time": 35,
        "end_time": 76,
        "parent_video_id": video.id,
    }
    sponsored_segment_create = SponsoredSegmentCreate(**first_segment_data)
    sponsored_segment = await sponsored_segment_repo.add(sponsored_segment_create, test_session)

    sponsor_data = {"sponsor_name": "Sponsor", "sponsored_segment_id": sponsored_segment.id}
    sponsorship_create = SponsorshipCreate(**sponsor_data)
    sponsorship = await sponsorship_repo.add(sponsorship_create, test_session)
    for field in base_fields + entity_fields:
        assert hasattr(sponsorship, field)
    for field in base_fields:
        assert getattr(sponsorship, field) is not None
    for k, v in sponsor_data.items():
        assert getattr(sponsorship, k) == v

    another_sponsor_data = {
        "sponsor_name": "Another Sponsor",
        "sponsored_segment_id": sponsored_segment.id,
    }
    sponsorship_create = SponsorshipCreate(**another_sponsor_data)
    with pytest.raises(IntegrityError):
        try:
            await sponsorship_repo.add(sponsorship_create, test_session)
        finally:
            await test_session.rollback()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id(test_session, sponsored_segment_repo, video_repo, sponsorship_repo):
    rand_uuid = "2df9f22f-a2e1-4498-940e-41c105a05f41"

    sponsorship = await sponsorship_repo.get_by_id(rand_uuid, test_session)
    assert sponsorship is None

    sponsorship = await sponsorship_repo.get_by_sponsorblock_id(rand_uuid, test_session)
    assert sponsorship is None

    sponsorship = await sponsorship_repo.get_by_segment_id(rand_uuid, test_session)
    assert sponsorship is None

    sponsorships = await sponsorship_repo.get_by_video_id(rand_uuid, test_session)
    assert sponsorships == []

    youtube_id = "7K1vBTMEYzk"
    video_data = VideoCreate(youtube_id=youtube_id)
    video = await video_repo.add(video_data, test_session)

    segment_data = [
        {
            "sponsorblock_id": "sponsorblockA",
            "start_time": 4,
            "end_time": 7,
            "parent_video_id": video.id,
        },
        {
            "sponsorblock_id": "sponsorblockB",
            "start_time": 8,
            "end_time": 100,
            "parent_video_id": video.id,
        },
    ]
    segments = []
    for data in segment_data:
        segment_create = SponsoredSegmentCreate(**data)
        segment = await sponsored_segment_repo.add(segment_create, test_session)
        segments.append(segment)

    sponsorship_data = [
        {
            "sponsor_name": "cool sponsor",
            "sponsor_description": "coolest ever sponsor",
            "sponsored_segment_id": segments[0].id,
        },
        {
            "sponsor_name": "coolest sponsor",
            "sponsor_description": "coolest coolest ever sponsor",
            "sponsored_segment_id": segments[1].id,
        },
    ]
    sponsorships = []
    for data in sponsorship_data:
        sponsorship_create = SponsorshipCreate(**data)
        sponsorship = await sponsorship_repo.add(sponsorship_create, test_session)
        sponsorships.append(sponsorship)

    for i, sponsorship in enumerate(sponsorships):
        queried_sponsorship = await sponsorship_repo.get_by_id(sponsorship.id, test_session)
        assert isinstance(queried_sponsorship, Sponsorship)
        assert sponsorship == queried_sponsorship

        queried_sponsorship = await sponsorship_repo.get_by_sponsorblock_id(
            segments[i].sponsorblock_id, test_session
        )
        assert isinstance(queried_sponsorship, Sponsorship)
        assert sponsorship == queried_sponsorship

        queried_sponsorship = await sponsorship_repo.get_by_segment_id(
            sponsorship.sponsored_segment_id, test_session
        )
        assert isinstance(queried_sponsorship, Sponsorship)
        assert sponsorship == queried_sponsorship

    queried_sponsorships = await sponsorship_repo.get_by_video_id(video.id, test_session)
    assert isinstance(queried_sponsorships, list) and all(
        isinstance(item, Sponsorship) for item in queried_sponsorships
    )
    assert queried_sponsorships == sponsorships


@pytest.mark.asyncio(loop_scope="session")
async def test_update(
    test_session, sponsored_segment_repo, video_repo, sponsorship_repo, base_fields, entity_fields
):
    retained_fields = ["id", "created_at", "sponsored_segment_id"]
    all_fields = base_fields + entity_fields
    changed_fields = [field for field in all_fields if field not in retained_fields]

    id = "a6945747-6dab-429e-a2cf-4c3d2f0e0727"
    await sponsorship_repo.update(id, SponsorshipUpdate(sponsor_name="blabla"), test_session)
    updated_sponsorship = await sponsorship_repo.get_by_id(id, test_session)
    assert updated_sponsorship is None

    video_data = {
        "youtube_id": "pHdJmDFYqTU",
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    segment_data = {
        "sponsorblock_id": "some_id",
        "start_time": 15,
        "end_time": 51,
        "parent_video_id": video.id,
    }
    segment_create = SponsoredSegmentCreate(**segment_data)
    segment = await sponsored_segment_repo.add(segment_create, test_session)

    original_sponsorship_data = {
        "sponsor_name": "advertiser",
        "sponsored_segment_id": segment.id,
    }
    sponsorship_create = SponsorshipCreate(**original_sponsorship_data)
    added_sponsorship = await sponsorship_repo.add(sponsorship_create, test_session)
    added_sponsorship_data = {
        k: v for k, v in added_sponsorship.__dict__.items() if k in all_fields
    }
    added_sponsorship_copy = Sponsorship(**added_sponsorship_data)

    new_sponsorship_data = {
        "sponsor_name": "better advertiser",
        "sponsor_description": "we sell good stuff",
        "sponsor_links": ["https://buy.me", "http://random.url"],
        "sponsor_coupon_code": "DISCOUNT",
        "sponsor_offer": "Only the best",
    }
    sponsorship_update = SponsorshipUpdate(**new_sponsorship_data)
    await sponsorship_repo.update(added_sponsorship.id, sponsorship_update, test_session)

    updated_sponsorship = await sponsorship_repo.get_by_id(added_sponsorship.id, test_session)
    await test_session.refresh(updated_sponsorship)
    assert isinstance(updated_sponsorship, Sponsorship)

    for field in retained_fields:
        assert getattr(added_sponsorship, field) == getattr(updated_sponsorship, field)
        assert getattr(added_sponsorship_copy, field) == getattr(updated_sponsorship, field)
    for field in changed_fields:
        assert getattr(added_sponsorship, field) == getattr(updated_sponsorship, field)
        assert getattr(added_sponsorship_copy, field) != getattr(updated_sponsorship, field)
        print(type(getattr(added_sponsorship_copy, field)))
        print(type(getattr(updated_sponsorship, field)))
        if field != "updated_at":
            assert getattr(updated_sponsorship, field) == new_sponsorship_data[field]
