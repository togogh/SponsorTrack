import pytest
from urllib.parse import urlencode
from requests import codes
from backend.repositories.all import VideoRepository
from backend.schemas.all import VideoCreate


@pytest.fixture
def video_repo():
    return VideoRepository()


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
    video_id = video.id

    response = await client.post(f"/videos/flag?{encoded_params}", json=request_body)
    assert response.status_code == codes.ok
    data = response.json()
    assert data["field_flagged"] == field_flagged

    request_params = {"video_id": video_id}
    response = await client.post(f"/videos/flag?{encoded_params}", json=request_body)
    assert response.status_code == codes.ok
    data = response.json()
    assert data["field_flagged"] == field_flagged
    assert data["status"] == "pending"

    request_body = {"field_flagged": "invalid_field"}
    response = await client.post(f"/videos/flag?{encoded_params}", json=request_body)
    assert response.status_code != codes.ok


# flag_sponsorship
# flag_sponsored_segment
