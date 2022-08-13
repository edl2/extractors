import requests, re
from urllib.parse import urlparse

from ..models.Extractor import Extractor
from ..models.Link import Link

class Topravideo(Extractor):
    def __init__(self) -> None:
        self.domains = ["topravideo.com", "vvtodmat.topravideo.com"]

    def get_link(self, url):
        video_id = urlparse(url).path.split("/")[-1]
        url = f"https://vvtodmat.topravideo.com/embed/{video_id}?autoplay=1&htmlplayer=1"
        r = requests.get(url).text
        re_m3u8 = re.findall(r"hls:'(.+?)'", r)
        return Link(address="https:" + re_m3u8[0])