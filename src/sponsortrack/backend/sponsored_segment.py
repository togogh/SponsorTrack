# import json


class SponsoredSegment:
    def __init__(self, start_time, end_time, segment_id, parent_video):
        self.start_time = start_time
        self.end_time = end_time
        self.segment_id = segment_id
        self.parent_video = parent_video
        self.transcript = ""

    # def extract_transcript(self):
    #     metadata = json.load(self.parent_video.metadata_path)
