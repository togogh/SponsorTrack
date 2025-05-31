from urllib.parse import urlparse, parse_qs
import requests
from requests.adapters import HTTPAdapter, Retry
import yt_dlp
import json
from pathlib import Path
from pydantic import HttpUrl
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api.formatters import JSONFormatter
import time
from datetime import date
import os

from sponsortrack.backend.sponsored_segment import SponsoredSegment
from sponsortrack.config import YOUTUBE_DOMAINS, SPONSORBLOCK_BASE_URL


class Video:
    def __init__(self, url: str):
        self.url: HttpUrl = url
        self.id: str = self.parse_id_from_url()
        self.download_path: Path
        self.sponsorblock_path: Path
        self.sponsorblock_data: list[dict]
        self.metadata_path: Path
        self.language: str
        self.title: str
        self.channel: str
        self.channel_id: str
        self.uploader_id: str
        self.upload_date: date
        self.description: str
        self.duration: int
        self.subtitles_path: Path
        self.sponsored_segments: list[SponsoredSegment]
        self.segments_path: Path

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

    @property
    def download_path(self):
        return self._download_path

    @download_path.setter
    def download_path(self, data_dir):
        path = Path(f"./{data_dir}/{self.id}")
        path.mkdir(exist_ok=True, parents=True)
        self._download_path = path

    def download_sponsorblock(self):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

        s.mount("http://", HTTPAdapter(max_retries=retries))
        url = f"{SPONSORBLOCK_BASE_URL}/api/skipSegments?videoID={self.id}"

        response = s.get(url)
        if response.status_code == 200:
            data = response.json()
        elif response.status_code == 404:
            raise ValueError(
                "This video has no sponsored segments marked with Sponsorblock. If this is a mistake, add them with https://sponsor.ajay.app/"
            )
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
            "format_sort": ["+size", "+br", "+res", "+fps"],
            "fragment_retries": 10,
            "retries": 10,
            "no_cache_dir": True,
            "cookies_from_browser": "chrome",
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove()
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
        self.channel = metadata["channel"]
        self.channel_id = metadata["channel_id"]
        self.uploader_id = metadata["uploader_id"]
        self.upload_date = metadata["upload_date"]
        self.description = metadata["description"]
        self.duration = metadata["duration"]

    def fetch_subtitles(self, retries=5, backoff_factor=0.1):
        for r in range(retries):
            try:
                proxy_config = WebshareProxyConfig(
                    proxy_username=os.getenv("WS_PROXY_UN"),
                    proxy_password=os.getenv("WS_PROXY_PW"),
                )
                ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
                subtitles = ytt_api.fetch(video_id=self.id, languages=[self.language])
                formatter = JSONFormatter()
                subtitles = formatter.format_transcript(subtitles, indent=4)
                return subtitles
            except Exception as e:
                print("Encountered error:", e)
                if r < retries:
                    print("Retrying...")
                    time.sleep(backoff_factor * (2 ** (r - 1)))

    def download_subtitles(self, skip_if_exists: bool = True):
        fp = Path(f"{self.download_path}/subtitles.json")
        if not (fp.exists() & skip_if_exists):
            subtitles = self.fetch_subtitles()
            with open(fp, "w") as f:
                f.write(subtitles)
        self.subtitles_path = fp

    def extract_sponsored_segments(self):
        segments = []
        for i, block in enumerate(self.sponsorblock_data):
            start_time = block["segment"][0]
            end_time = block["segment"][1]
            segment_id = block["UUID"]
            order = i

            segment = SponsoredSegment(start_time, end_time, segment_id, order, self)
            segments.append(segment)
        self.sponsored_segments = segments

    def enrich_sponsored_segments(self):
        for segment in self.sponsored_segments:
            segment.extract_subtitles()
            segment.extract_sponsor_info()

    def save_sponsored_segments(self):
        segments_info = []
        for segment in self.sponsored_segments:
            segments_info.append(segment.to_dict())

        fp = Path(f"{self.download_path}/segments.json")
        with open(fp, "w") as f:
            json.dump(segments_info, f, indent=4, sort_keys=True)

        self.segments_path = fp

    def fetch_segments_info(self, data_dir="data"):
        self.download_path = data_dir

        fp = Path(f"{self.download_path}/segments.json")
        if not fp.exists():
            self.download_sponsorblock()
            self.download_metadata()
            self.download_subtitles()
            self.extract_sponsored_segments()
            self.enrich_sponsored_segments()
            self.save_sponsored_segments()

        with open(fp, "r") as f:
            segments_info = json.load(f)

        return segments_info
