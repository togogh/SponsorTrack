from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
from requests.adapters import HTTPAdapter, Retry
import yt_dlp
import json
from pathlib import Path

from sponsortrack.config import YOUTUBE_DOMAINS, SPONSORBLOCK_BASE_URL


class Video:
    def __init__(self, url):
        self.url = url
        self.id = self.parse_id_from_url()
        self.download_path = ""
        self.sponsorblock_path = ""
        self.metadata_path = ""

    def parse_id_from_url(self):
        parse_result = urlparse(self.url)

        # Check if url is a youtube url
        if parse_result.netloc not in YOUTUBE_DOMAINS:
            raise ValueError("Input url isn't a valid youtube url")

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

    def update_download_path(self):
        path = Path(f"./data/{self.id}")
        path.mkdir(exist_ok=True)
        self.download_path = path

    def download_sponsorblock(self):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

        s.mount("http://", HTTPAdapter(max_retries=retries))
        url = f"{SPONSORBLOCK_BASE_URL}/api/skipSegments?videoID={self.id}"

        response = s.get(url)
        if response.status_code == 200:
            data = response.json()
        elif response.status_code == 404:
            raise ValueError("No data from Sponsorblock")
        else:
            raise ConnectionError("Can't connect to Sponsorblock")

        fp = Path(f"{self.download_path}/sponsorblock.json")
        with open(fp, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)

        self.sponsorblock_path = fp

    def download_metadata(self):
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "no_warnings": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                metadata = ydl.sanitize_info(info)
        except yt_dlp.utils.DownloadError:
            raise ConnectionError("Can't connect to yt_dlp")

        fp = Path(f"{self.download_path}/metadata.json")
        with open(fp, "w") as f:
            json.dump(metadata, f, indent=4, sort_keys=True)

        self.metadata_path = fp

    def fetch_info(self):
        self.update_download_path()
        self.download_sponsorblock()
        self.download_metadata()
