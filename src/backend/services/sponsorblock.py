import requests
from requests.adapters import HTTPAdapter, Retry
from backend.core.constants import constants
from fastapi import HTTPException


async def download_sponsorblock(video_id: str) -> dict:
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

    s.mount("https://", HTTPAdapter(max_retries=retries))
    url = f"{constants.SPONSORBLOCK_BASE_URL}/api/skipSegments?videoID={video_id}"

    response = s.get(url)
    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="This video has no sponsored segments marked with Sponsorblock. If this is a mistake, add them with https://sponsor.ajay.app/",
        )
    else:
        raise HTTPException(status_code=503, detail="Can't connect to Sponsorblock")

    return data
