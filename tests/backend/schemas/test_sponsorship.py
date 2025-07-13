from backend.schemas.sponsorship import SponsorshipUpdate
from pydantic import ValidationError
import pytest


@pytest.mark.parametrize(
    "sponsor_links, expected_error",
    [
        pytest.param(
            ["https://www.bbc.com/news/world-asia-12345678", "https://vimeo.com/123456"], None
        ),
        pytest.param(["not_a_url", "https://vimeo.com/123456"], ValidationError),
        pytest.param("https://vimeo.com/123456", ValidationError),
    ],
)
async def test_validate_sponsor_links(sponsor_links, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            SponsorshipUpdate(sponsor_links=sponsor_links)
    else:
        sponsorship = SponsorshipUpdate(sponsor_links=sponsor_links)
        assert sponsorship.sponsor_links == sponsor_links
        assert all(isinstance(e, str) for e in sponsorship.sponsor_links)
