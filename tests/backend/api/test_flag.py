import pytest
from urllib.parse import urlencode
from requests import codes
from backend.repositories.all import (
    VideoRepository,
    SponsoredSegmentRepository,
    SponsorshipRepository,
)
from backend.schemas.all import VideoCreate, SponsoredSegmentCreate, SponsorshipCreate


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
async def test_flag_video(video_repo, client, test_session):
    youtube_id = "MwLbGcUMy6g"
    field_flagged = "channel"
    request_params = {"youtube_id": youtube_id}
    request_body = {"field_flagged": field_flagged}
    encoded_params = urlencode(request_params)
    response = await client.post(f"/videos/flag?{encoded_params}", json=request_body)
    assert response.status_code != codes.ok

    video = await video_repo.add(VideoCreate(youtube_id=youtube_id), test_session)

    response = await client.post(f"/videos/flag?{encoded_params}", json=request_body)
    assert response.status_code == codes.ok
    data = response.json()
    assert data["field_flagged"] == field_flagged

    request_params = {"video_id": video.id}
    encoded_params = urlencode(request_params)
    response = await client.post(f"/videos/flag?{encoded_params}", json=request_body)
    assert response.status_code == codes.ok
    data = response.json()
    assert data["field_flagged"] == field_flagged
    assert data["status"] == "pending"

    request_body = {"field_flagged": "invalid_field"}
    response = await client.post(f"/videos/flag?{encoded_params}", json=request_body)
    assert response.status_code != codes.ok


@pytest.mark.asyncio(loop_scope="session")
async def test_flag_sponsored_segment(
    video_repo, sponsored_segment_repo, sponsorship_repo, client, test_session
):
    random_uuid = "a50d14be-e55b-42af-bce6-5831bb75f73b"
    field_flagged = "subtitles"
    request_params = {"sponsored_segment_id": random_uuid}
    request_body = {"field_flagged": field_flagged}
    encoded_params = urlencode(request_params)
    response = await client.post(
        f"/videos/sponsored-segments/flag?{encoded_params}", json=request_body
    )
    assert response.status_code != codes.ok

    youtube_id = "_8rBQ4kxayU"
    video = await video_repo.add(VideoCreate(youtube_id=youtube_id), test_session)
    sponsored_segment = await sponsored_segment_repo.add(
        SponsoredSegmentCreate(start_time=0, end_time=10, parent_video_id=video.id), test_session
    )

    request_params = {"sponsored_segment_id": sponsored_segment.id}
    encoded_params = urlencode(request_params)
    response = await client.post(
        f"/videos/sponsored-segments/flag?{encoded_params}", json=request_body
    )
    assert response.status_code == codes.ok
    data = response.json()
    assert data["field_flagged"] == field_flagged

    sponsorship = await sponsorship_repo.add(
        SponsorshipCreate(sponsor_name="Sponsor", sponsored_segment_id=sponsored_segment.id),
        test_session,
    )

    request_params = {"sponsorship_id": sponsorship.id}
    encoded_params = urlencode(request_params)
    response = await client.post(
        f"/videos/sponsored-segments/flag?{encoded_params}", json=request_body
    )
    assert response.status_code == codes.ok
    data = response.json()
    assert data["field_flagged"] == field_flagged
    assert data["status"] == "pending"

    request_body = {"field_flagged": "invalid_field"}
    response = await client.post(
        f"/videos/sponsored-segments/flag?{encoded_params}", json=request_body
    )
    assert response.status_code != codes.ok


# flag_sponsorship
