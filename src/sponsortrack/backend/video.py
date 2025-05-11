from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import yt_dlp

from sponsortrack.config import YOUTUBE_DOMAINS

class Video:
    def __init__(self, url):
        self.url = url
        self.id = self.parse_id_from_url()
        self.metadata = None
    
    def parse_id_from_url(self):
        parse_result = urlparse(self.url)
        
        if parse_result.netloc not in YOUTUBE_DOMAINS:
            raise ValueError("Input url isn't a valid youtube url")
        
        print(parse_result)
        try:
            if parse_result.path == '/watch':
                video_id = parse_qs(parse_result.query)['v'][0]
            elif parse_result.netloc == "youtu.be":
                video_id = parse_result.path.split('/')[1]
            elif parse_result.path.startswith("/embed/"):
                video_id = parse_result.path.split("/embed/")[1]
            elif parse_result.path.startswith("/shorts/"):
                video_id = parse_result.path.split("/shorts/")[1]
        except:
            raise ValueError("Input url doesn't contain a valid video id")

        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise ValueError("Input url doesn't contain a valid video id")
        except:
            raise ValueError("Input url doesn't contain a valid video id")
            
        # ydl_opts = {
        #     'quiet': True,
        #     'skip_download': True,
        #     'no_warnings': True,
        # }
        # try:
        #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #         info = ydl.extract_info(self.url, download=False)
        #         self.metadata = json.dumps(ydl.sanitize_info(info))
        # except yt_dlp.utils.DownloadError:
        #     raise ValueError("Input url doesn't contain valid video id")
        
        # video_check_url = f"http://gdata.youtube.com/feeds/api/videos/{video_id}"
        # response = requests.get(video_check_url)
        # print(response.status_code)
        # if response.status_code != 200:
        #     raise ValueError("Input url doesn't contain valid video id")
        
        return video_id