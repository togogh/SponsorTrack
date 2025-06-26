from pydantic import HttpUrl
from urllib.parse import urlparse, parse_qs
from fastapi import HTTPException
from backend.core.settings import ws_settings
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api.formatters import JSONFormatter
import time
import json
import pandas as pd


async def extract_id_from_url(url: HttpUrl) -> str:
    # Extract video id from url

    parse_result = urlparse(str(url))

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
        raise HTTPException(status_code=400, detail="Input url doesn't contain a valid video id")

    try:
        return video_id
    except UnboundLocalError:
        raise HTTPException(status_code=400, detail="Input url doesn't contain a valid video id")


async def download_metadata(youtube_id):
    if ws_settings.WS_PROXY_UN and ws_settings.WS_PROXY_PW:
        proxy_str = f"http://{ws_settings.WS_PROXY_UN}:{ws_settings.WS_PROXY_PW}@p.webshare.io:80/"
    else:
        proxy_str = ""

    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        "format_sort": ["+size", "+br", "+res", "+fps"],
        "fragment_retries": 10,
        "retries": 10,
        "no_cache_dir": True,
        "proxy": proxy_str,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info = ydl.extract_info(youtube_url, download=False)
            metadata = ydl.sanitize_info(info)
    except yt_dlp.utils.DownloadError:
        raise HTTPException(
            status_code=404,
            detail="Can't connect to yt_dlp",
        )

    return metadata


async def fetch_transcript(youtube_id, language, retries=1, backoff_factor=0.1):
    if ws_settings.WS_PROXY_UN and ws_settings.WS_PROXY_PW:
        proxy_config = WebshareProxyConfig(
            proxy_username=ws_settings.WS_PROXY_UN,
            proxy_password=ws_settings.WS_PROXY_PW,
        )
        ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
    else:
        ytt_api = YouTubeTranscriptApi()
    if language is None:
        transcript_list = ytt_api.list(youtube_id)
        language = list(transcript_list)[0].language_code
    for r in range(retries):
        try:
            transcript = ytt_api.fetch(video_id=youtube_id, languages=[language])
            formatter = JSONFormatter()
            transcript = formatter.format_transcript(transcript, indent=4)
            transcript = json.loads(transcript)
            return transcript, language
        except Exception as e:
            print("Encountered error:", e)
            if r < retries:
                print("Retrying...")
                time.sleep(backoff_factor * (2 ** (r - 1)))


async def map_transcript_to_segment_subtitles(transcript: str, segment):
    df = pd.DataFrame(transcript)
    start_row = df[df["start"] <= segment.start_time].iloc[-1]
    max_start_time = df["start"].max()
    if segment.end_time <= max_start_time:
        end_row = df[df["start"] >= segment.end_time].iloc[0]
    else:
        end_row = df.iloc[-1]
    df = df.iloc[start_row.name : end_row.name]
    text = " ".join(df["text"].tolist())
    return text
