from backend.services.video_sponsorship.video_metadata import download_metadata
from backend.schemas.all import MetadataJson


async def test_download_metadata():
    youtube_id = "RTr2bu9ugJU"
    metadata_data = await download_metadata(youtube_id)
    assert isinstance(metadata_data, dict)
    try:
        MetadataJson(**metadata_data)
    except Exception:
        raise AssertionError("Metadata object doesn't have essential keys")
