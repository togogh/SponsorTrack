import pytest
from sponsortrack.backend.video import Video
from pathlib import Path
import json
import os


class TestVideo:
    @pytest.mark.parametrize(
        "input,output,error_msg",
        [
            ("https://www.youtube.com/watch?v=2oZzUeNGr78", "2oZzUeNGr78", None),
            ("https://youtu.be/2oZzUeNGr78", "2oZzUeNGr78", None),
            ("https://youtube.com/embed/2oZzUeNGr78", "2oZzUeNGr78", None),
            ("https://youtube.com/shorts/2oZzUeNGr78", "2oZzUeNGr78", None),
            (
                "https://www.youtube.com/watch?v=2oZzUeNGr78&feature=shared",
                "2oZzUeNGr78",
                None,
            ),
            ("https://www.google.com", ValueError, "Input url isn't a valid youtube url"),
            (None, ValueError, "Input url isn't a valid youtube url"),
            ("invalid input", ValueError, "Input url isn't a valid youtube url"),
            (
                "https://youtube.com/watch?invalid=parameter",
                ValueError,
                "Input url doesn't contain a valid video id",
            ),
            (
                "https://youtube.com/watch?v=invalid-id-too-long",
                ValueError,
                "Input url doesn't contain a valid video id",
            ),
        ],
    )
    def test_parse_id_from_url(self, input, output, error_msg):
        if output is ValueError:
            with pytest.raises(ValueError, match=error_msg):
                video = Video(input)
        else:
            video = Video(input)
            assert video.id == output

    @pytest.mark.parametrize(
        "input,output",
        [
            ("https://youtu.be/2oZzUeNGr78", Path("./tests/data/2oZzUeNGr78")),
        ],
    )
    def test_update_download_path(self, input, output):
        video = Video(input)
        video.download_path = "tests/data"
        assert video.download_path == output
        assert video.download_path.exists()

    @pytest.mark.parametrize(
        "url,metadata_path,language,title,channel_id,channel,uploader_id,upload_date,description,duration",
        [
            (
                "https://youtu.be/YDsXNM_KmpY",
                Path("./tests/data/YDsXNM_KmpY/metadata.json"),
                "fil",
                "House Trends 2025 That You Can Make Gaya Para Estetik Your House",
                "UCHHYB05slIGQR5NT92EPr5g",
                "Oliver Austria",
                "@OliverAustria",
                "20250315",
                "Gawin nating maganda ang bahay nyo mah dudes!!\n\nFor business inquiries E-mail: austriallyan@gmail.com\n\nAt dahil madaming nagtatanong, eto pala Camera gear ko:\nCameras: \nhttps://bit.ly/32KHWBt\nLens:\nhttps://bit.ly/326xNMY\nRed Mic:\nhttps://bit.ly/2HlvRe5\nOn-Camera Mic\nhttps://bit.ly/2pa8J9h\nAudio Recorder:\nhttps://bit.ly/2oyYYkU\nTripod:\nhttps://bit.ly/2M6bL7o\nStanding Desk\nhttps://bit.ly/3hOMifp\n\nDisclaimer:\nThis video is for entertainment purposes only. All the information and tips mentioned in the video is based on my personal experience, your results may vary. For your Plans and Designs get an Architect.",
                658,
            ),
            (
                "https://www.youtube.com/watch?v=ofKe4b169ts",
                Path("./tests/data/ofKe4b169ts/metadata.json"),
                "en",
                "The REAL Kitchen Nightmares | Reading Reddit Stories",
                "UCYJPby9DRCteedh5tfxVbrw",
                "Smosh Pit",
                "@smoshpit",
                "20250517",
                "These tales from servers will blow your mind. Start listening and discover what\u2019s beyond the edge of your seat. New members can try Audible now free for 30 days and dive into a world of new thrills. Visit https://Audible.com/SRRS or text (SRRS) to 500-500.\n\nPODCAST:\nhttps://smo.sh/PitRedditSpotify\nhttps://smo.sh/PitRedditiHeart\nhttps://smo.sh/PitRedditApple\n\n0:00 Intro\n1:16 A lady called to warn us about her husband https://www.reddit.com/r/TalesFromYourServer/comments/1iarl4n/a_lady_called_to_warn_us_about_her_husband/\n11:24 Sponsor\n12:41 She wrote a mean note on the tip https://www.reddit.com/r/TalesFromYourServer/comments/1jzxky4/woman_wrote_dont_be_such_a_c_on_tip_line_after_i/\n18:43 My best friend is broke but won't take the job I'm offering https://www.reddit.com/r/BestofRedditorUpdates/comments/1itqo6r/my_m31_best_friend_m33_is_broke_ive_been_offering/\n36:08 Snitched on my coworker who spit in food https://www.reddit.com/r/AmItheAsshole/comments/mnh20i/aita_for_snitching_on_a_coworker_for_spitting_on/\n46:45 My mom's rude customer turned out to be my gf https://www.reddit.com/r/relationship_advice/comments/hoznlr/my_moms_rude_customer_turned_out_to_be_my/\n1:08:37 I still remember his Hawaiian shirt https://www.reddit.com/r/TalesFromYourServer/comments/1fnsfob/i_still_remember_his_hawaiian_shirt/\n\nSUBSCRIBE: https://smo.sh/Sub2SmoshPit\n\nWEAR OUR JOKES: https://smosh.com\n\nWHO YOU SEE\nShayne Topp // https://www.instagram.com/shaynetopp/\nTommy Bowe // https://www.instagram.com/tomeybones/\nChanse McCrary // https://www.instagram.com/phatchanse/\n\nWHO YOU DON\u2019T SEE (usually)\nDirector: Emily Rose Jacobson\nEditor: Vida Robbins\nDirector of Programming, Smosh Pit: Emily Rose Jacobson\nAssociate Producer, Smosh Pit: Bailey Petracek\nProduction Designer: Cassie Vance\nArt Director: Erin Kuschner\nAssistant Art Director: Josie Bellerby\nStage Manager: Alex Aguilar\nProp Master: Courtney Chapman\nArt Coordinator: Abby Schmidt\nWardrobe Assistant: Elizabeth Park\nProp Assistant: Bridgette Baron\nAudio Mixer: Scott Neff\nAudio Utility: Dina Ramli\nDirector of Photography: James Hull\nCamera Operator: Ryan Blewett\nCamera Operator: Macy Armstrong\nAssistant Director: Jonathan Hyon\nExecutive Vice President of Production: Amanda Barnes\nSenior Production Manager: Alexcina Figueroa\nProduction Manager: Jonathan Hyon\nProduction Coordinator: Zianne Hoover\nOperations & Production Coordinator: Oliver Wehlander\nProduction Assistant: Caroline Smith\nPost Production Manager: Luke Baker\nDIT/Lead AE: Matt Duran\nIT: Tim Baker\nIT & Equipment Coordinator: Lopati Ho Chee\nSound Editor: Gareth Hird\nDirector of Design: Brittany Hobbs\nSenior Motion & Branding Designer: Christie Hauck\nGraphic Designers: Ness Cardano, Monica Ravitch\nSenior Manager, Channel & Strategy: Lizzy Jones\nChannel Operations Coordinator: Audrey Carganilla\nDirector of Social Media: Erica Noboa\nSocial Creative Producer: Peter Ditzler, Tommy Bowe\nMerchandising Manager: Mallory Myers\nSocial Media Coordinator: Kim Wilborn\nBrand Partnership Manager: Chloe Mays\nOperations Manager: Selina Garcia\nPeople Operations Specialist: Katie Fink\nFront Office Assistant: Sara Faltersack\nCEO: Alessandra Catanese\nExecutive Producers: Anthony Padilla, Ian Hecox\nEVP of Programming: Kiana Parker\nCoordinating Producer of Programming: Marcus Munguia\nAssociate Producer, Special Projects: Rachel Collis\nExecutive Assistant: Katelyn Hempstead\n\n\nOTHER SMOSHES:\nSmosh: https://smo.sh/Sub2Smosh\nSmosh Games: https://smo.sh/Sub2SmoshGames\nSmoshCast: https://smo.sh/Sub2SmoshCast\n\nFOLLOW US:\nTikTok: https://smo.sh/TikTok\nInstagram: https://instagram.com/smosh\nFacebook: https://facebook.com/smosh\"",
                4399,
            ),
        ],
    )
    def test_download_metadata(
        self,
        url,
        metadata_path,
        language,
        title,
        channel_id,
        channel,
        uploader_id,
        upload_date,
        description,
        duration,
    ):
        video = Video(url)
        video.download_path = "tests/data"
        video.download_metadata()

        # Metadata path should match expected path
        assert video.metadata_path == metadata_path

        # File should exist
        assert video.metadata_path.exists()

        with open(video.metadata_path, "r") as f:
            metadata = json.load(f)

            # File should not be empty
            assert len(metadata) > 0

            # Channel id should be correct
            assert metadata["language"] == language
            assert metadata["title"] == title
            assert metadata["channel_id"] == channel_id
            assert metadata["channel"] == channel
            assert metadata["uploader_id"] == uploader_id
            assert metadata["upload_date"] == upload_date
            assert metadata["description"] == description
            assert metadata["duration"] == duration

    @pytest.mark.parametrize(
        "url,sponsorblock_path,len_sponsorblock,error,error_msg",
        [
            (
                "https://youtu.be/CPk8Bh4soSQ",
                Path("./tests/data/CPk8Bh4soSQ/sponsorblock.json"),
                1,
                None,
                None,
            ),
            (
                "https://www.youtube.com/watch?v=NBbWEl76qX4",
                Path("./tests/data/NBbWEl76qX4/metadata.json"),
                0,
                ValueError,
                "This video has no sponsored segments marked with Sponsorblock. If this is a mistake, add them with https://sponsor.ajay.app/",
            ),
            (
                "https://www.youtube.com/watch?v=zJp824Oi_40&t=2082s",
                Path("./tests/data/zJp824Oi_40/sponsorblock.json"),
                2,
                None,
                None,
            ),
        ],
    )
    def test_download_sponsorblock(
        self, url, sponsorblock_path, len_sponsorblock, error, error_msg
    ):
        video = Video(url)
        video.download_path = "tests/data"
        if error is not None:
            with pytest.raises(error, match=error_msg):
                video.download_sponsorblock()
        else:
            video.download_sponsorblock()

            # Sponsorblock path should match expected path
            assert video.sponsorblock_path == sponsorblock_path

            # File should exist
            assert video.sponsorblock_path.exists()

            # Sponsorblock data should exist
            assert video.sponsorblock_data is not None
            assert len(video.sponsorblock_data) == len_sponsorblock

            with open(video.sponsorblock_path, "r") as f:
                sponsorblock = json.load(f)

                # File should have expected num of sponsors
                assert len(sponsorblock) == len_sponsorblock

    @pytest.mark.parametrize(
        "url,subtitles_path",
        [
            (
                "https://youtu.be/CPk8Bh4soSQ",
                Path("./tests/data/CPk8Bh4soSQ/subtitles.json"),
            ),
            (
                "https://youtu.be/ofKe4b169ts",
                Path("./tests/data/ofKe4b169ts/subtitles.json"),
            ),
            (
                "https://youtu.be/zJp824Oi_40",
                Path("./tests/data/zJp824Oi_40/subtitles.json"),
            ),
        ],
    )
    def test_download_subtitles(self, url, subtitles_path):
        video = Video(url)
        video.download_path = "tests/data"
        video.download_metadata()
        video.download_subtitles()

        # Subtitles path should match expected path
        assert video.subtitles_path == subtitles_path

        # File should exist
        assert video.subtitles_path.exists()

        with open(video.subtitles_path, "r") as f:
            subtitles = json.load(f)

            # File should not be empty
            assert len(subtitles) > 0

        # Make sure subtitles are overwritten if not skip_if_exists
        subtitles_last_modified = os.path.getmtime(subtitles_path)
        video.download_subtitles(skip_if_exists=False)
        assert subtitles_last_modified != os.path.getmtime(subtitles_path)

    @pytest.mark.parametrize(
        "url,len_segments,start_time,end_time,segment_id,order,parent_video_id",
        [
            (
                "https://youtu.be/CPk8Bh4soSQ",
                1,
                1981,
                2048.1,
                "97565687886b1dd6d4399a092720ea347681d1bfa9dafc5fe6b12cda279384687",
                0,
                "CPk8Bh4soSQ",
            ),
            (
                "https://www.youtube.com/watch?v=zJp824Oi_40&t=2082s",
                2,
                2365.947,
                2456.54,
                "7249034829e10fbec5338cb9f675c1065f271c451d51798bbcfb76b9404264727",
                1,
                "zJp824Oi_40",
            ),
        ],
    )
    def test_extract_sponsored_segments(
        self,
        url,
        len_segments,
        start_time,
        end_time,
        segment_id,
        order,
        parent_video_id,
    ):
        video = Video(url)
        video.download_path = "tests/data"
        video.download_sponsorblock()
        video.extract_sponsored_segments()

        # Segments should exist
        assert video.sponsored_segments is not None

        # Should have expected number of segments
        assert len(video.sponsored_segments) == len_segments

        # Check that segment values are correct
        segment = video.sponsored_segments[order]
        assert start_time == segment.start_time
        assert end_time == segment.end_time
        assert segment_id == segment.segment_id
        assert order == segment.order
        assert parent_video_id == segment.parent_video.id

        # # Path should match expected path
        # assert video.segments_path == segments_path

        # # File should exist
        # assert video.segments_path.exists()

        # with open(video.segments_path, "r") as f:
        #     segments = json.load(f)

        #     # File should have expected num of sponsors
        #     assert len(segments) == len_segments
