from backend.services.video_sponsorship.sponsored_segments import (
    download_sponsorblock,
    get_sponsored_segments,
    get_or_create_sponsored_segments,
)
from backend.repositories.all import (
    VideoRepository,
    SponsoredSegmentRepository,
    SponsorshipRepository,
)
from backend.models.all import SponsoredSegment
from backend.schemas.all import VideoCreate, SponsorshipCreate, SponsoredSegmentCreate
import pytest
from fastapi.exceptions import HTTPException


@pytest.fixture
def video_repo():
    return VideoRepository()


@pytest.fixture
def sponsored_segment_repo():
    return SponsoredSegmentRepository()


@pytest.fixture
def sponsorship_repo():
    return SponsorshipRepository()


@pytest.mark.parametrize(
    "youtube_id, len_blocks, error",
    [
        ("1-_AhiAPyZg", 0, HTTPException),
        ("BsBSgtkmjak", 2, None),
    ],
)
async def test_download_sponsorblock(youtube_id, len_blocks, error):
    if error is not None:
        with pytest.raises(error):
            await download_sponsorblock(youtube_id)
    else:
        blocks = await download_sponsorblock(youtube_id)
        assert len(blocks) == len_blocks


@pytest.mark.asyncio(loop_scope="session")
async def test_get_sponsored_segments(
    test_session, sponsored_segment_repo, sponsorship_repo, video_repo
):
    with pytest.raises(ValueError):
        try:
            await get_sponsored_segments(test_session, sponsored_segment_repo, None, None)
        finally:
            await test_session.rollback()

    random_uuid = "1ad77a49-8e8b-4bc4-8639-990da8f46f38"

    response_segments = await get_sponsored_segments(
        test_session, sponsored_segment_repo, random_uuid, None
    )
    assert len(response_segments) == 0

    response_segments = await get_sponsored_segments(
        test_session, sponsored_segment_repo, None, random_uuid
    )
    assert len(response_segments) == 0

    youtube_id = "PbWVbQQwWJo"
    video = await video_repo.add(VideoCreate(youtube_id=youtube_id), test_session)
    segments_data = [
        {
            "start_time": 83,
            "end_time": 124,
            "parent_video_id": video.id,
        },
        {
            "start_time": 174,
            "end_time": 198,
            "parent_video_id": video.id,
        },
    ]
    segments = []
    for data in segments_data:
        segment = await sponsored_segment_repo.add(SponsoredSegmentCreate(**data), test_session)
        segments.append(segment)

    sponsorship = await sponsorship_repo.add(
        SponsorshipCreate(sponsor_name="A Sponsor", sponsored_segment_id=segments[0].id),
        test_session,
    )

    response_segments = await get_sponsored_segments(
        test_session, sponsored_segment_repo, sponsorship.id, None
    )
    assert len(response_segments) == 1
    assert response_segments[0] == segments[0]

    response_segments = await get_sponsored_segments(
        test_session, sponsored_segment_repo, None, video.id
    )
    assert len(response_segments) == 2
    response_segment_ids = [s.id for s in response_segments]
    for segment in segments:
        assert segment.id in response_segment_ids

    with pytest.raises(ValueError):
        try:
            await get_sponsored_segments(
                test_session, sponsored_segment_repo, sponsorship.id, video.id
            )
        finally:
            await test_session.rollback()


@pytest.mark.parametrize(
    "youtube_id, len_segments, error",
    [
        ("R3blSsMfMwU", 3, None),
        ("fLlSVk2IS5E", 0, HTTPException),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_or_create_sponsored_segments(
    youtube_id, len_segments, error, test_session, sponsored_segment_repo, video_repo
):
    video = await video_repo.add(VideoCreate(youtube_id=youtube_id), test_session)
    if error is not None:
        with pytest.raises(error):
            try:
                segments = await get_or_create_sponsored_segments(
                    video, test_session, sponsored_segment_repo
                )
            finally:
                await test_session.rollback()
    else:
        segments = await get_or_create_sponsored_segments(
            video, test_session, sponsored_segment_repo
        )
        assert isinstance(segments, list) and all(
            isinstance(item, SponsoredSegment) for item in segments
        )
        assert len(segments) == len_segments
