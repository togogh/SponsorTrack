from backend.schemas.sponsored_segment import SponsoredSegmentUpdate
from pydantic import ValidationError
import pytest


@pytest.mark.parametrize(
    "start_time, end_time, expected_error",
    [
        pytest.param(10, 15, None),
        pytest.param(None, None, None),
        pytest.param(None, 5, None),
        pytest.param(1, None, None),
        pytest.param(19, 5, ValidationError),
    ],
)
async def test_validate_times(start_time, end_time, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            SponsoredSegmentUpdate(start_time=start_time, end_time=end_time)
    else:
        sponsored_segment = SponsoredSegmentUpdate(start_time=start_time, end_time=end_time)
        assert start_time == sponsored_segment.start_time
        assert end_time == sponsored_segment.end_time
