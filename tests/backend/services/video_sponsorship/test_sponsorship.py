from backend.services.video_sponsorship.sponsorship import (
    get_sponsorships,
    create_prompt,
    create_sponsorships,
)
from backend.repositories.all import (
    VideoRepository,
    SponsoredSegmentRepository,
    SponsorshipRepository,
    GeneratedSponsorshipRepository,
)
from backend.schemas.all import VideoCreate, SponsorshipCreate, SponsoredSegmentCreate, MetadataJson
from backend.models.all import Sponsorship, SponsoredSegment, GeneratedSponsorship
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
        language="my",
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
        metadata.channel,
        metadata.description,
        metadata.upload_date,
        metadata.language,
        segment.subtitles,
    ]
    for v in values_given:
        assert v in prompt


@pytest.mark.parametrize(
    "youtube_id, metadata, segments_data, sponsors",
    [
        (
            "OYGh07D8QBU",
            {
                "language": "en",
                "title": "How to Learn Python in 10 Minutes",
                "upload_date": "2024-05-01",
                "description": "In this video, we'll cover the basics of Python programming for beginners. Great for getting started quickly!",
                "duration": 612.5,  # in seconds (10 minutes and 12.5 seconds)
                "channel": "CodeAcademy Official",
            },
            [
                {
                    "sponsorblock_id": "abc123xyz789",
                    "start_time": 120.5,
                    "end_time": 145.8,
                    "subtitles": "This video is sponsored by SkillBoost, the fastest way to learn new skills online.",
                },
                {
                    "sponsorblock_id": "segment_456",
                    "start_time": 30.0,
                    "end_time": 60.0,
                    "subtitles": "Big thanks to EcoBottle for supporting this episode. Check them out at the link below.",
                },
            ],
            ["SkillBoost", "EcoBottle"],
        ),
        (
            "iOMefWteXzA",
            {
                "language": "ja",
                "title": "【初心者向け】Python入門講座",
                "upload_date": "2023-11-15",
                "description": "Pythonの基礎を日本語でわかりやすく解説します。",
                "duration": 1430.0,
                "channel": "Japanese Dev Hub",
            },
            [
                {
                    "sponsorblock_id": "jpseg100",
                    "start_time": 60.5,
                    "end_time": 89.2,
                    "subtitles": "この動画は、株式会社みらい教育の提供でお送りします。",
                    "parent_video_id": "01f4be37-1111-4d2e-bb3b-8d6167e037df",
                }
            ],
            ["株式会社みらい教育"],
        ),
        (
            "S4eIhg2aTys",
            {
                "language": None,
                "title": "Unboxing the New iPhone 15 Pro Max!",
                "upload_date": "2025-01-20",
                "description": "Join me as I unbox and review Apple's latest flagship phone.",
                "duration": 845.2,
                "channel": "TechTastic",
            },
            [],
            [],
        ),
        (
            "dX_F8cRi7-E",
            {
                "language": "en",
                "title": "Exploring Portugal’s Hidden Beaches 🌊",
                "upload_date": "2024-09-12",
                "description": (
                    "This video is brought to you by WanderMate — your personal trip planner.\n"
                    "Plan smarter trips at https://wandermate.app"
                ),
                "duration": 1025.0,
                "channel": "GlobeTrek Diaries",
            },
            [
                {
                    "sponsorblock_id": "seg-wander-001",
                    "start_time": 60.0,
                    "end_time": 90.0,
                    "subtitles": "",
                },
            ],
            ["WanderMate"],
        ),
        (
            "ZBk8oCmfpMg",
            {
                "language": "fr",
                "title": "Ma routine du matin en français 🇫🇷",
                "upload_date": "2025-03-11",
                "description": "Je vous montre comment je commence ma journée tout en pratiquant le français. Pas de marques, juste ma vraie routine.",
                "duration": 675.0,
                "channel": "LinguaLuna",
            },
            [
                {
                    "sponsorblock_id": None,
                    "start_time": 30.0,
                    "end_time": 120.0,
                    "subtitles": "Alors je commence ma journée avec un café…",
                },
            ],
            [],
        ),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_create_sponsorships(
    youtube_id,
    metadata,
    segments_data,
    sponsors,
    video_repo,
    sponsored_segment_repo,
    test_session,
    sponsorship_repo,
    generated_sponsorship_repo,
):
    video = await video_repo.add(VideoCreate(youtube_id=youtube_id), test_session)
    metadata = MetadataJson(**metadata)
    segments = []
    for data in segments_data:
        data["parent_video_id"] = video.id
        segment = await sponsored_segment_repo.add(SponsoredSegmentCreate(**data), test_session)
        segments.append(segment)

    sponsorships = await create_sponsorships(
        segments, metadata, sponsorship_repo, generated_sponsorship_repo, test_session
    )
    assert len(sponsorships) == len(sponsors)
    assert isinstance(sponsorships, list) and all(
        isinstance(item, Sponsorship) for item in sponsorships
    )
    found_sponsors = [sponsorship.sponsor_name for sponsorship in sponsorships]
    assert set(found_sponsors) == set(sponsors)

    for sponsorship in sponsorships:
        generated_sponsorships = await generated_sponsorship_repo.get_by_sponsorship_id(
            sponsorship.id, test_session
        )
        assert isinstance(generated_sponsorships, list) and all(
            isinstance(item, GeneratedSponsorship) for item in generated_sponsorships
        )
        for generated_sponsorship in generated_sponsorships:
            assert sponsorship.sponsor_name == generated_sponsorship.sponsor_name
