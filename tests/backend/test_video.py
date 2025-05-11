import pytest
from sponsortrack.backend.video import Video

@pytest.mark.parametrize("input,output,error_msg", [
    ("https://www.youtube.com/watch?v=2oZzUeNGr78", "2oZzUeNGr78", None),
    ("https://youtu.be/2oZzUeNGr78", "2oZzUeNGr78", None),
    ("https://youtube.com/embed/2oZzUeNGr78", "2oZzUeNGr78", None),
    ("https://youtube.com/shorts/2oZzUeNGr78", "2oZzUeNGr78", None),
    ("https://www.youtube.com/watch?v=2oZzUeNGr78&feature=shared", "2oZzUeNGr78", None),
    ("https://www.google.com", ValueError, "Input url isn't a valid youtube url"),
    ("invalid input", ValueError, "Input url isn't a valid youtube url"),
    ("https://youtube.com/watch?invalid=parameter", ValueError, "Input url doesn't contain a valid video id"),
    ("https://youtube.com/watch?v=invalid-id-too-long", ValueError, "Input url doesn't contain a valid video id"),
])
def test_parse_id_from_url(input, output, error_msg):
    if output == ValueError:
        with pytest.raises(ValueError, match=error_msg):        
            video = Video(input)
    else:   
        video = Video(input)
        assert video.id == output
    

