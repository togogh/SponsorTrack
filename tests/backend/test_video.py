import pytest
from sponsortrack.backend.video import Video
from pathlib import Path
import json


@pytest.mark.parametrize(
    "input,output,error_msg",
    [
        ("https://www.youtube.com/watch?v=2oZzUeNGr78", "2oZzUeNGr78", None),
        ("https://youtu.be/2oZzUeNGr78", "2oZzUeNGr78", None),
        ("https://youtube.com/embed/2oZzUeNGr78", "2oZzUeNGr78", None),
        ("https://youtube.com/shorts/2oZzUeNGr78", "2oZzUeNGr78", None),
        (
            "https://www.youtube.com/watch?v=2oZzUeNGr78&feature=shared",
            "2oZzUeNGr78",
            None,
        ),
        ("https://www.google.com", ValueError, "Input url isn't a valid youtube url"),
        (None, ValueError, "Input url isn't a valid youtube url"),
        ("invalid input", ValueError, "Input url isn't a valid youtube url"),
        (
            "https://youtube.com/watch?invalid=parameter",
            ValueError,
            "Input url doesn't contain a valid video id",
        ),
        (
            "https://youtube.com/watch?v=invalid-id-too-long",
            ValueError,
            "Input url doesn't contain a valid video id",
        ),
    ],
)
def test_parse_id_from_url(input, output, error_msg):
    if output is ValueError:
        with pytest.raises(ValueError, match=error_msg):
            video = Video(input)
    else:
        video = Video(input)
        assert video.id == output


@pytest.mark.parametrize(
    "input,output",
    [
        ("https://youtu.be/2oZzUeNGr78", Path("./data/2oZzUeNGr78")),
    ],
)
def test_update_download_path(input, output):
    video = Video(input)
    video.update_download_path()
    assert video.download_path == output
    assert video.download_path.exists()


@pytest.mark.parametrize(
    "url,metadata_path,channel_id",
    [
        (
            "https://youtu.be/2oZzUeNGr78",
            Path("./data/2oZzUeNGr78/metadata.json"),
            "@comfortlevelpodcast",
        ),
        (
            "https://www.youtube.com/watch?v=NBbWEl76qX4",
            Path("./data/NBbWEl76qX4/metadata.json"),
            "@YNABofficial",
        ),
    ],
)
def test_download_metadata(url, metadata_path, channel_id):
    video = Video(url)
    video.update_download_path()
    video.download_metadata()

    # Metadata path should match expected path
    assert video.metadata_path == metadata_path

    # File should exist
    assert video.metadata_path.exists()

    with open(video.metadata_path, "r") as f:
        metadata = json.load(f)

        # File should not be empty
        assert len(metadata) > 0

        # Channel id should be correct
        assert metadata["uploader_id"] == channel_id


@pytest.mark.parametrize(
    "url,sponsorblock_path,len_sponsorblock,error,error_msg",
    [
        (
            "https://youtu.be/CPk8Bh4soSQ",
            Path("./data/CPk8Bh4soSQ/sponsorblock.json"),
            1,
            None,
            None,
        ),
        (
            "https://www.youtube.com/watch?v=NBbWEl76qX4",
            Path("./data/NBbWEl76qX4/metadata.json"),
            0,
            ValueError,
            "No data from Sponsorblock",
        ),
        (
            "https://www.youtube.com/watch?v=zJp824Oi_40&t=2082s",
            Path("./data/zJp824Oi_40/sponsorblock.json"),
            2,
            None,
            None,
        ),
    ],
)
def test_download_sponsorblock(url, sponsorblock_path, len_sponsorblock, error, error_msg):
    video = Video(url)
    video.update_download_path()
    if error is not None:
        with pytest.raises(error, match=error_msg):
            video.download_sponsorblock()
    else:
        video.download_sponsorblock()

        # Sponsorblock path should match expected path
        assert video.sponsorblock_path == sponsorblock_path

        # File should exist
        assert video.sponsorblock_path.exists()

        # Sponsorblock data should exist
        assert video.sponsorblock_data is not None
        assert len(video.sponsorblock_data) == len_sponsorblock

        with open(video.sponsorblock_path, "r") as f:
            sponsorblock = json.load(f)

            # File should not be empty
            assert len(sponsorblock) == len_sponsorblock
