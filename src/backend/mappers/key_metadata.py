from backend.schemas.video import VideoUpdateMetadata
from datetime import datetime


async def map_key_metadata(metadata: dict) -> VideoUpdateMetadata:
    return VideoUpdateMetadata(
        language=metadata["language"],
        title=metadata["title"],
        upload_date=datetime.strptime(metadata["upload_date"], "%Y%m%d"),
        description=metadata["description"],
        duration=metadata["duration"],
    )
