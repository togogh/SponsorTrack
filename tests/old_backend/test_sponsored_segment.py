from sponsortrack.backend.sponsored_segment import SponsoredSegment
import pytest
from unittest.mock import Mock
from pathlib import Path


class TestSponsoredSegment:
    @pytest.mark.parametrize(
        "subtitles_path,start_time,end_time,subtitles",
        [
            (
                Path(r".\tests\data\CPk8Bh4soSQ\subtitles.json"),
                1981,
                2048.1,
                """- And so it's not a slow thing. Today's "Reddit Stories" is
brought to you by HelloFresh. HelloFresh makes home cooking
fun, easy, and affordable thanks to their farm fresh
pre-portioned ingredients delivered right to your door. It makes it so much easier. You get to cut out searching
online for the right recipe, going to the grocery store
and picking out ingredients. Sometimes you have to buy a whole jar for just one tablespoon that
you need for the recipe. It just is all delivered
right to your door at the right portions that
you need for that recipe. And it's so delicious. Plus they have tons of options. They've got fit and wholesome,
vegetarian, family friendly, quick and easy, anything
to suit your needs. And you can make veggie and protein swaps. So whatever you want, they got it. We got a box scent here once, and it was amazing how
quick and easy it was. And it was so delicious. Made two perfect portions,
and it was awesome. So for free breakfast for life, go to hellofresh.com/freepitreddit. One free breakfast item per box while subscription is active. That's free breakfast for life just by going to
hellofresh.com/freepitreddit. HelloFresh. America's number one meal kit. Back to the show.""",
            ),
            (
                Path(r".\tests\data\zJp824Oi_40\subtitles.json"),
                2365.947,
                2456.54,
                "taste. Hold the phone, boys. Let me just come in here real quick and tell you about today's sponsor, Shopify. If you guys don't know, uh me, Joey Bizinger of Trash Taste, have a clothing brand. It's called nonsense. Even though I had all of these dope ass designs that I wanted to sell to people all over the world, I had no idea how to do it. I don't know how to run an e-commerce site. I don't know how to operate a storefront. I didn't know any of that. Luckily, there was Shopify. Shopify is the commerce platform behind millions of businesses around the world and 10% of all e-commerce in the US. From household names like Mattel and Gym Shark to brands just getting started. Get started with your own design studio with hundreds of readytouse templates. Shopify helps you build a beautiful online store to match your brand style. Shopify is packed with helpful AI tools that write product descriptions, page headlines, and even enhance your product photography. You can easily create email and social media campaigns wherever your customers are scrolling or scrolling. And best yet, Shopify is your commerce expert with world-class expertise in everything from managing inventory to international shipping to processing returns and beyond. As I mentioned, uh, Nonsense has been around for pretty much coming up to 3 years now, and we still use Shopify. We've used it from the beginning. We still use it now because it just works. So, if you're ready to sell, you're ready for Shopify. Turn your big business idea into cha-ching with Shopify on your side. Sign up for your $1 per month trial period and start selling today at shopify.com/trash. Go to shopify.com/trash. Shopify.com/trash. Back to the episode.",
            ),
        ],
    )
    def test_extract_subtitles(self, subtitles_path, start_time, end_time, subtitles):
        mock_video = Mock()
        mock_video.subtitles_path = subtitles_path
        segment = SponsoredSegment(start_time, end_time, "", "", mock_video)
        segment.extract_subtitles()
        assert subtitles == segment.subtitles
