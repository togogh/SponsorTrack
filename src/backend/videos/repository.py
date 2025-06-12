class VideoRepository:
    def get_video_sponsorship(self, id: str) -> dict:
        fake_db = {
            "v5SDSWscaKY": {"youtube_id": "v5SDSWscaKY", "sponsorship_info": "Example"},
        }
        return fake_db.get(id)
