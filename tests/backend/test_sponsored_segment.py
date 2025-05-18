from sponsortrack.backend.video import Video
import pytest


@pytest.mark.parametrize(
    "url",
    [
        ("https://www.youtube.com/watch?v=zJp824Oi_40&t=2082s"),
        ("https://youtu.be/CPk8Bh4soSQ"),
    ],
)
def test_extract_subtitles(url):
    video = Video(url)
    video.fetch_info()
    video.extract_sponsored_segments()
    for segment in video.sponsored_segments:
        segment.extract_subtitles()
        assert len(segment.subtitles) > 0
