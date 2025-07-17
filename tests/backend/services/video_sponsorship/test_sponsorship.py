from backend.services.video_sponsorship.sponsorship import (
    get_sponsorships,
    create_prompt,
    create_sponsorships,  # noqa: F401
)
from backend.repositories.all import (
    VideoRepository,
    SponsoredSegmentRepository,
    SponsorshipRepository,
)
from backend.schemas.all import VideoCreate, SponsorshipCreate, SponsoredSegmentCreate, MetadataJson
from backend.models.all import Sponsorship, SponsoredSegment
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


@pytest.mark.asyncio(loop_scope="session")
async def test_get_sponsorships(test_session, sponsored_segment_repo, sponsorship_repo, video_repo):
    rand_uuid = "39fb588f-5db5-4597-9887-fa11d074492e"
    sponsorships = await get_sponsorships(rand_uuid, sponsorship_repo, test_session)
    assert sponsorships == []

    youtube_id = "l2dDbs0qpd8"
    video = await video_repo.add(VideoCreate(youtube_id=youtube_id), test_session)

    segments_data = [
        {
            "start_time": 91,
            "end_time": 512,
            "parent_video_id": video.id,
        },
        {
            "start_time": 756,
            "end_time": 999,
            "parent_video_id": video.id,
        },
    ]
    segments = []
    for data in segments_data:
        segment = await sponsored_segment_repo.add(SponsoredSegmentCreate(**data), test_session)
        segments.append(segment)

    sponsorships_data = [
        {
            "sponsor_name": "Asioid",
            "sponsored_segment_id": segments[0].id,
        },
        {
            "sponsor_name": "aoIOFSF",
            "sponsored_segment_id": segments[0].id,
        },
        {
            "sponsor_name": "MASODFISAHDG",
            "sponsored_segment_id": segments[1].id,
        },
        {
            "sponsor_name": "Asioid",
            "sponsored_segment_id": segments[1].id,
        },
        {
            "sponsor_name": "MASOIFHASDD",
            "sponsored_segment_id": segments[1].id,
        },
    ]
    sponsorships = []
    for data in sponsorships_data:
        sponsorship = await sponsorship_repo.add(SponsorshipCreate(**data), test_session)
        sponsorships.append(sponsorship)

    response_sponsorships = await get_sponsorships(video.id, sponsorship_repo, test_session)
    assert len(response_sponsorships) == 5
    assert isinstance(response_sponsorships, list) and all(
        isinstance(item, Sponsorship) for item in response_sponsorships
    )

    response_sponsorships = [
        {
            "sponsor_name": sponsorship.sponsor_name,
            "sponsored_segment_id": sponsorship.sponsored_segment_id,
        }
        for sponsorship in response_sponsorships
    ]
    for sponsorship in response_sponsorships:
        assert sponsorship in sponsorships_data


async def test_create_prompt():
    metadata = MetadataJson(
        language="me",
        title="A Video",
        upload_date="2021-02-09",
        description="A video indeed. Make sure to buy Me's products at me.com/more",
        duration=902.4,
        channel="Us",
    )
    segment = SponsoredSegment(
        start_time=9.3,
        end_time=10.2,
        subtitles="This is sponsored by Me, who is the best person ever",
        parent_video_id="21c00a5e-dffc-4197-ab85-5bbf23c644a1",
    )
    prompt = await create_prompt(metadata, segment)
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    values_given = [
        metadata["channel"],
        metadata["description"],
        metadata["upload_date"],
        metadata["language"],
        segment.subtitles,
    ]
    for v in values_given:
        assert v in prompt
