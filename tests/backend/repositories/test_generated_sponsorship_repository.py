from backend.repositories.all import (
    SponsoredSegmentRepository,
    VideoRepository,
    SponsorshipRepository,
    GeneratedSponsorshipRepository,
)
from backend.schemas.all import (
    SponsoredSegmentCreate,
    VideoCreate,
    SponsorshipCreate,
    GeneratedSponsorshipCreate,
    GeneratedSponsorshipUpdate,
)
from backend.models.all import GeneratedSponsorship
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
def generated_sponsorship_repo():
    return GeneratedSponsorshipRepository()


@pytest.fixture
def entity_fields():
    return list(GeneratedSponsorshipCreate.__pydantic_fields__.keys())


@pytest.mark.asyncio(loop_scope="session")
async def test_add(
    test_session,
    sponsored_segment_repo,
    video_repo,
    sponsorship_repo,
    generated_sponsorship_repo,
    base_fields,
    entity_fields,
):
    youtube_id = "0SQor2z2QAU"
    video_data = {
        "youtube_id": youtube_id,
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    first_segment_data = {
        "start_time": 38,
        "end_time": 94,
        "parent_video_id": video.id,
    }
    sponsored_segment_create = SponsoredSegmentCreate(**first_segment_data)
    sponsored_segment = await sponsored_segment_repo.add(sponsored_segment_create, test_session)

    sponsor_data = {"sponsor_name": "Sponsor", "sponsored_segment_id": sponsored_segment.id}
    sponsorship_create = SponsorshipCreate(**sponsor_data)
    sponsorship = await sponsorship_repo.add(sponsorship_create, test_session)

    generated_sponsor_data = {
        "sponsor_name": "Sponsor",
        "generator": "llm",
        "model": "agi",
        "provider": "the void",
        "sponsorship_id": sponsorship.id,
    }
    generated_sponsorship_create = GeneratedSponsorshipCreate(**generated_sponsor_data)
    generated_sponsorship = await generated_sponsorship_repo.add(
        generated_sponsorship_create, test_session
    )
    for field in base_fields + entity_fields:
        assert hasattr(generated_sponsorship, field)
    for field in base_fields:
        assert getattr(generated_sponsorship, field) is not None
    for k, v in generated_sponsor_data.items():
        assert getattr(generated_sponsorship, k) == v

    another_gen_data = {
        "sponsor_name": "Sponsor",
        "generator": "llmSUPREME",
        "model": "AGI",
        "provider": "the void",
        "sponsorship_id": sponsorship.id,
    }
    generated_sponsorship_create = GeneratedSponsorshipCreate(**another_gen_data)
    generated_sponsorship = await generated_sponsorship_repo.add(
        generated_sponsorship_create, test_session
    )
    for field in base_fields + entity_fields:
        assert hasattr(generated_sponsorship, field)
    for field in base_fields:
        assert getattr(generated_sponsorship, field) is not None
    for k, v in another_gen_data.items():
        assert getattr(generated_sponsorship, k) == v


@pytest.mark.asyncio(loop_scope="session")
async def test_get_by_id(
    test_session, sponsored_segment_repo, video_repo, sponsorship_repo, generated_sponsorship_repo
):
    rand_uuid = "2df9f22f-a2e1-4498-940e-41c105a05f41"

    sponsorship = await generated_sponsorship_repo.get_by_id(rand_uuid, test_session)
    assert sponsorship is None

    sponsorships = await generated_sponsorship_repo.get_by_sponsorship_id(rand_uuid, test_session)
    assert sponsorships == []

    youtube_id = "u7WaC429YcU"
    video_data = VideoCreate(youtube_id=youtube_id)
    video = await video_repo.add(video_data, test_session)

    segment_data = {
        "sponsorblock_id": "oaishdga",
        "start_time": 9,
        "end_time": 10,
        "parent_video_id": video.id,
    }
    segment_create = SponsoredSegmentCreate(**segment_data)
    segment = await sponsored_segment_repo.add(segment_create, test_session)

    sponsorship_data = [
        {
            "sponsor_name": "cool sponsor",
            "sponsored_segment_id": segment.id,
        },
        {
            "sponsor_name": "coolest sponsor",
            "sponsored_segment_id": segment.id,
        },
    ]
    sponsorships = []
    for data in sponsorship_data:
        sponsorship_create = SponsorshipCreate(**data)
        sponsorship = await sponsorship_repo.add(sponsorship_create, test_session)
        sponsorships.append(sponsorship)

    generated_sponsorship_data = [
        {
            "sponsor_name": "Sponsor",
            "generator": "llmSUPREME",
            "model": "AGI",
            "provider": "the void",
            "sponsorship_id": sponsorships[0].id,
        },
        {
            "sponsor_name": "Sponsor",
            "generator": "llmSUPREME",
            "model": "AGI",
            "provider": "the void",
            "sponsorship_id": sponsorships[1].id,
        },
    ]
    generated_sponsorships = []
    for data in generated_sponsorship_data:
        generated_sponsorship_create = GeneratedSponsorshipCreate(**data)
        generated_sponsorship = await generated_sponsorship_repo.add(
            generated_sponsorship_create, test_session
        )
        generated_sponsorships.append(generated_sponsorship)

    for i, generated_sponsorship in enumerate(generated_sponsorships):
        queried_generated_sponsorship = await generated_sponsorship_repo.get_by_id(
            generated_sponsorship.id, test_session
        )
        assert isinstance(queried_generated_sponsorship, GeneratedSponsorship)
        assert generated_sponsorship == queried_generated_sponsorship

        queried_generated_sponsorships = await generated_sponsorship_repo.get_by_sponsorship_id(
            sponsorships[i].id, test_session
        )
        assert isinstance(queried_generated_sponsorships, list) and all(
            isinstance(item, GeneratedSponsorship) for item in queried_generated_sponsorships
        )
        assert queried_generated_sponsorships == [generated_sponsorships[i]]


@pytest.mark.asyncio(loop_scope="session")
async def test_update(
    test_session,
    sponsored_segment_repo,
    video_repo,
    sponsorship_repo,
    generated_sponsorship_repo,
    base_fields,
    entity_fields,
):
    retained_fields = ["id", "created_at", "sponsorship_id"]
    all_fields = base_fields + entity_fields
    changed_fields = [field for field in all_fields if field not in retained_fields]

    id = "a6945747-6dab-429e-a2cf-4c3d2f0e0727"
    await generated_sponsorship_repo.update(
        id, GeneratedSponsorshipUpdate(sponsor_name="blabla"), test_session
    )
    updated_generated_sponsorship = await generated_sponsorship_repo.get_by_id(id, test_session)
    assert updated_generated_sponsorship is None

    video_data = {
        "youtube_id": "OHnkdW9myP0",
    }
    video_create = VideoCreate(**video_data)
    video = await video_repo.add(video_create, test_session)

    segment_data = {
        "sponsorblock_id": "a new id",
        "start_time": 125,
        "end_time": 1225,
        "parent_video_id": video.id,
    }
    segment_create = SponsoredSegmentCreate(**segment_data)
    segment = await sponsored_segment_repo.add(segment_create, test_session)

    sponsorship_data = {
        "sponsor_name": "advertiser",
        "sponsored_segment_id": segment.id,
    }
    sponsorship_create = SponsorshipCreate(**sponsorship_data)
    sponsorship = await sponsorship_repo.add(sponsorship_create, test_session)

    original_generated_sponsorship_data = {
        "sponsor_name": "advertiser",
        "generator": "llmSUPREME",
        "model": "AGI",
        "provider": "the void",
        "sponsorship_id": sponsorship.id,
    }
    generated_sponsorship_create = GeneratedSponsorshipCreate(**original_generated_sponsorship_data)
    added_generated_sponsorship = await generated_sponsorship_repo.add(
        generated_sponsorship_create, test_session
    )
    added_generated_sponsorship_data = {
        k: v for k, v in added_generated_sponsorship.__dict__.items() if k in all_fields
    }
    added_generated_sponsorship_copy = GeneratedSponsorship(**added_generated_sponsorship_data)

    new_generated_sponsorship_data = {
        "sponsor_name": "better advertiser",
        "sponsor_description": "we sell good stuff",
        "sponsor_links": ["https://buy.me", "http://random.url"],
        "sponsor_coupon_code": "DISCOUNT",
        "sponsor_offer": "Only the best",
        "generator": "new boy",
        "model": "sssh",
        "provider": "aloha",
        "prompt": "do this",
        "sponsorship_id": sponsorship.id,
    }
    generated_sponsorship_update = GeneratedSponsorshipUpdate(**new_generated_sponsorship_data)
    await generated_sponsorship_repo.update(
        added_generated_sponsorship.id, generated_sponsorship_update, test_session
    )

    updated_generated_sponsorship = await generated_sponsorship_repo.get_by_id(
        added_generated_sponsorship.id, test_session
    )
    await test_session.refresh(updated_generated_sponsorship)
    assert isinstance(updated_generated_sponsorship, GeneratedSponsorship)

    for field in retained_fields:
        assert getattr(added_generated_sponsorship, field) == getattr(
            updated_generated_sponsorship, field
        )
        assert getattr(added_generated_sponsorship_copy, field) == getattr(
            updated_generated_sponsorship, field
        )
    for field in changed_fields:
        assert getattr(added_generated_sponsorship, field) == getattr(
            updated_generated_sponsorship, field
        )
        assert getattr(added_generated_sponsorship_copy, field) != getattr(
            updated_generated_sponsorship, field
        )
        if field != "updated_at":
            assert (
                getattr(updated_generated_sponsorship, field)
                == new_generated_sponsorship_data[field]
            )
