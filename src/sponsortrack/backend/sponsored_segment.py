import pandas as pd


class SponsoredSegment:
    def __init__(self, start_time, end_time, segment_id, order, parent_video):
        self.start_time = start_time
        self.end_time = end_time
        self.segment_id = segment_id
        self.order = order
        self.parent_video = parent_video
        self.subtitles = ""

    def extract_subtitles(self):
        df = pd.read_json(self.parent_video.subtitles_path)
        start_row = df[df["start"] <= self.start_time].iloc[-1]
        end_row = df[df["start"] >= self.end_time].iloc[0]
        df = df.iloc[start_row.name : end_row.name]
        text = " ".join(df["text"].tolist())
        self.subtitles = text
