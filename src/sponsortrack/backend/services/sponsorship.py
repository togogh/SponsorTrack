from urllib.parse import urlparse, parse_qs
import requests

class SponsorshipService:
    def __init__(self, sponsorship_repo):
        self.sponsorship_repo = sponsorship_repo

    async def parse_id_from_url(self, url):
        parse_result = urlparse(url)

        # Extract video id from url
        try:
            if parse_result.path == "/watch":
                video_id = parse_qs(parse_result.query)["v"][0]
            elif parse_result.netloc == "youtu.be":
                video_id = parse_result.path.split("/")[1]
            elif parse_result.path.startswith("/embed/"):
                video_id = parse_result.path.split("/embed/")[1]
            elif parse_result.path.startswith("/shorts/"):
                video_id = parse_result.path.split("/shorts/")[1]
        except Exception:
            raise ValueError("Input url doesn't contain a valid video id")

        # Check if video id belongs to an actual youtube video
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise ValueError("Input url doesn't contain a valid video id")
        except Exception:
            raise ValueError("Input url doesn't contain a valid video id")

        return video_id
    
    async def