import requests, re, base64
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta, datetime

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..scanners.m3u8_src import scan_page

class WatchNBAStreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["live.watchnbastreams.com", "nbastreamswatch.com"]
        self.name = "WatchNBAStreams"
    
    def get_link(self, url):
        m3u8 = ""
        video_html = requests.get(url).text
        video = BeautifulSoup(video_html, "html.parser")
        if len(video.find_all("iframe")) > 0:
            iframe = video.find("iframe").get("src")
            r_iframe = requests.get(iframe).text
            atob = re.findall(r'window.atob\("(.+?)"\)', r_iframe)[0]
            m3u8 = Link(address=base64.b64decode(atob).decode("utf-8"), headers={"User-Agent": self.user_agent, "Referer": iframe})
            return m3u8