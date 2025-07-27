import pytest
from urllib.parse import urlencode
from requests import codes


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
        (
            {"id": "9sTsI4tpATk"},
            "9sTsI4tpATk",
            ["Factor", "Sakuraco", "Shopify", "Zocdoc"],
        ),
        (
            {"id": "YjdGQZpG9lk"},
            "YjdGQZpG9lk",
            ["Surfshark VPN", "Surfshark VPN"],
        ),
        (
            {"url": "https://www.youtube.com/watch?v=BYizgB2FcAQ"},
            "BYizgB2FcAQ",
            ["Ground News", "NordVPN"],
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
        assert sorted(sponsors) == sorted(expected_sponsors)
