from backend.schemas.video import VideoUpdate
from datetime import datetime


async def map_key_metadata(metadata: dict) -> VideoUpdate:
    return VideoUpdate(
        language=metadata["language"],
        title=metadata["title"],
        upload_date=datetime.strptime(metadata["upload_date"], "%Y%m%d"),
        description=metadata["description"],
        duration=metadata["duration"],
    )
