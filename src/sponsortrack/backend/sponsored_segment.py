import pandas as pd
from pathlib import Path


class SponsoredSegment:
    def __init__(
        self, start_time, end_time, segment_id, order, parent_subtitles_path, parent_video_id
    ):
        self.start_time: float = start_time
        self.end_time: float = end_time
        self.segment_id: str = segment_id
        self.order: int = order
        self.parent_subtitles_path: Path = parent_subtitles_path
        self.parent_video_id: str = parent_video_id
        self.subtitles: str = self.extract_subtitles()

    def extract_subtitles(self):
        df = pd.read_json(self.parent_subtitles_path)
        start_row = df[df["start"] <= self.start_time].iloc[-1]
        end_row = df[df["start"] >= self.end_time].iloc[0]
        df = df.iloc[start_row.name : end_row.name]
        text = " ".join(df["text"].tolist())
        return text

    def get_info(self):
        info = {
            "parent_video_id": self.parent_video_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "segment_id": self.segment_id,
            "order": self.order,
            "subtitles": self.subtitles,
        }
        return info
