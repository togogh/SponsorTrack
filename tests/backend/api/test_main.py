from httpx import AsyncClient, ASGITransport
from backend.main import app
import pytest
from backend.routers.video_sponsorship import session_dependency
from urllib.parse import urlencode
from requests import codes


@pytest.fixture(scope="session")
async def client(test_session):
    async def override_session_dependency():
        yield test_session

    app.dependency_overrides[session_dependency] = override_session_dependency
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.mark.parametrize(
    "params, expected_youtube_id, expected_sponsors",
    [
        (
            {"id": "6ovuMoW2EGk"},
            "6ovuMoW2EGk",
            [
                "Ground News",
                "NordVPN",
                "Built",
                "Alma",
            ],
        ),
        (
            {"url": "https://www.youtube.com/watch?v=6ovuMoW2EGk"},
            "6ovuMoW2EGk",
            [
                "Ground News",
                "NordVPN",
                "Built",
                "Alma",
            ],
        ),
        (
            {"url": "https://www.youtube.com/watch?v=xD2ulhw-_D8"},
            "xD2ulhw-_D8",
            [
                "DeleteMe",
                "DeleteMe",
            ],
        ),
        ({"id": "bPJSsAr2iu0"}, "bPJSsAr2iu0", []),
        (
            {"id": "bPJSsAr2iu0", "url": "https://www.youtube.com/watch?v=bPJSsAr2iu0"},
            "bPJSsAr2iu0",
            None,
        ),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_video_sponsorships(params, expected_youtube_id, expected_sponsors, client):
    encoded_params = urlencode(params)
    response = await client.get(f"/videos/sponsorships/?{encoded_params}")
    if expected_sponsors is None:
        assert response.status_code != codes.ok
    else:
        assert response.status_code == codes.ok
        data = response.json()
        assert data["youtube_id"] == expected_youtube_id
        assert len(data["sponsorships"]) == len(expected_sponsors)
        sponsors = [s["sponsor_name"] for s in data["sponsorships"]]
        assert set(sponsors) == set(expected_sponsors)
