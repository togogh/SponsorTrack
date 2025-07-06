from backend.repositories.all import VideoRepository
from backend.schemas.all import VideoCreate
import pytest
from sqlalchemy.exc import IntegrityError


@pytest.mark.usefixtures("test_session")
@pytest.mark.asyncio(loop_scope="class")
class TestVideoRepository:
    @classmethod
    def setup_class(cls):
        cls.base_fields = ["id", "created_at", "updated_at"]
        cls.video_fields = [
            "youtube_id",
            "language",
            "title",
            "upload_date",
            "description",
            "duration",
            "channel",
        ]
        cls.repo = VideoRepository()

    @pytest.mark.parametrize(
        "input, expected_values, error",
        [
            pytest.param(
                VideoCreate(youtube_id="IInciWyU74U"),
                {"youtube_id": "IInciWyU74U"},
                None,
                id="valid_insert",
            ),
            pytest.param(
                VideoCreate(youtube_id="IInciWyU74U"), None, IntegrityError, id="duplicate_video"
            ),
        ],
    )
    async def test_add(self, input, expected_values, error):
        assert hasattr(self, "session")
        if error is not None:
            with pytest.raises(error):
                await self.repo.add(input, self.session)
        else:
            video = await self.repo.add(input, self.session)
            for field in self.base_fields + self.video_fields:
                assert hasattr(video, field)
            for field in self.base_fields:
                assert getattr(video, field) is not None
            for k, v in expected_values.items():
                assert getattr(video, k) == v
