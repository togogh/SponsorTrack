import pandas as pd
from typing import TYPE_CHECKING
from sponsortrack.backend.generators.select_generator import select_generator
import re
import json


if TYPE_CHECKING:
    from sponsortrack.backend.video import Video


class SponsoredSegment:
    def __init__(self, start_time, end_time, segment_id, order, parent_video):
        self.start_time: float = start_time
        self.end_time: float = end_time
        self.segment_id: str = segment_id
        self.order: int = order
        self.parent_video: Video = parent_video
        self.subtitles: str
        self.sponsor_info: dict

    def extract_subtitles(self):
        df = pd.read_json(self.parent_video.subtitles_path)
        start_row = df[df["start"] <= self.start_time].iloc[-1]
        max_start_time = df["start"].max()
        if self.end_time <= max_start_time:
            end_row = df[df["start"] >= self.end_time].iloc[0]
        else:
            end_row = df.iloc[-1]
        df = df.iloc[start_row.name : end_row.name]
        text = " ".join(df["text"].tolist())
        self.subtitles = text

    def craft_prompt(self):
        prompt = f"""
            I have a sponsored segment cut from a Youtube video. Here's some information about this segment:

            Youtube channel: {self.parent_video.channel}
            Video description: {self.parent_video.description}
            Upload date: {self.parent_video.upload_date}
            Video language: {self.parent_video.language}
            Segment subtitles: {self.subtitles}

            Given this information, could you give me information about the sponsor? I want you to return a json with the following information:

            sponsor_name: Name of the sponsor
            sponsor_description: What the sponsor does or provides
            sponsor_offer: Any discounts or coupons provided by the sponsor
            sponsor_links: List of websites related to the sponsor, such as affiliate links, homepages, or links to the offer

            Please respond with just the json.
        """
        return prompt

    def extract_sponsor_info(self):
        generator = select_generator()
        generator.connect_client()
        generator.queue_message("user", self.craft_prompt())
        generator.generate_response()
        response = generator.messages[-1]["content"]
        match = re.search(r"json\s*(\{.*?\})\s*", response, re.DOTALL)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            self.sponsor_info = data
        else:
            raise ValueError("No JSON found.")

    def to_dict(self, skip=["parent_video"]):
        if skip is None:
            skip = []
        data = {k: v for k, v in self.__dict__.items() if k not in skip}
        data["parent_video_id"] = self.parent_video.id
        return data
