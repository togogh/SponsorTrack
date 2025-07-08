from backend.schemas.sponsored_segment import SponsoredSegmentUpdate
from pydantic import ValidationError
import pytest


@pytest.mark.parametrize(
    "start_time, end_time, duration, expected_error",
    [
        pytest.param(10, 15, 5, None),
        pytest.param(10, 15, 3, ValidationError),
        pytest.param(15, 10, 5, ValidationError),
        pytest.param(None, None, None, None),
        pytest.param(None, 5, 3, None),
        pytest.param(1, 5, None, None),
        pytest.param(19, 5, None, ValidationError),
    ],
)
async def test_validate_times(start_time, end_time, duration, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            SponsoredSegmentUpdate(start_time=start_time, end_time=end_time, duration=duration)
    else:
        sponsored_segment = SponsoredSegmentUpdate(
            start_time=start_time, end_time=end_time, duration=duration
        )
        assert start_time == sponsored_segment.start_time
        assert end_time == sponsored_segment.end_time
        assert duration == sponsored_segment.duration
