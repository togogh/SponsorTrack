from urllib.parse import urlparse, parse_qs
import requests
from requests.adapters import HTTPAdapter, Retry
import yt_dlp
import json
from pathlib import Path
from pydantic import HttpUrl
from youtube_transcript_api import YouTubeTranscriptApi

from sponsortrack.backend.sponsored_segment import SponsoredSegment
from sponsortrack.config import YOUTUBE_DOMAINS, SPONSORBLOCK_BASE_URL


class Video:
    def __init__(self, url: str):
        self.url: HttpUrl = url
        self.id: str = self.parse_id_from_url()
        self.download_path: Path = None
        self.sponsorblock_path: Path = None
        self.sponsorblock_data: list[dict] = None
        self.metadata_path: Path = None
        self.language: str = ""
        self.title: str = ""
        self.channel_id: str = ""
        self.uploader_id: str = ""
        self.description: str = ""
        self.duration: int = 0
        self.subtitles_path: Path = None
        self.sponsored_segments: list[SponsoredSegment] = []

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
        self.sponsorblock_data = data

    def download_metadata(self):
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "no_warnings": True,
            "format": "best",
            "format_sort": ["+size", "+br", "+res", "+fps"],
            "fragment_retries": 10,
            "retries": 10,
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

        self.language = metadata["language"]
        self.title = metadata["title"]
        self.channel_id = metadata["channel_id"]
        self.uploader_id = metadata["uploader_id"]
        self.description = metadata["description"]
        self.duration = metadata["duration"]

    def download_subtitles(self, skip_if_exists: bool = True):
        fp = Path(f"{self.download_path}/subtitles.json")
        if not (fp.exists() & skip_if_exists):
            ytt_api = YouTubeTranscriptApi()
            subtitles = ytt_api.fetch(video_id=self.id, languages=[self.language])
            with open(fp, "w") as f:
                json.dump(subtitles, f, indent=4, sort_keys=True)
        self.subtitles_path = fp

    def fetch_info(self):
        self.update_download_path()
        self.download_sponsorblock()
        self.download_metadata()
        self.download_subtitles()

    def extract_sponsored_segments(self):
        segments = []
        for i, block in enumerate(self.sponsorblock_data):
            start_time = block["segment"][0]
            end_time = block["segment"][1]
            segment_id = i
            parent_video = self
            segments.append(SponsoredSegment(start_time, end_time, segment_id, parent_video))
        self.sponsored_segments = segments
