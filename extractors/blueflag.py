import requests, re
from ..models.Extractor import Extractor
from . import sawlive

class Blueflag(Extractor):
    def __init__(self) -> None:
        self.domains = ["blueflag.ga", "www.blueflag.ga"]

    def get_link(self, url):
        r = requests.get(url, headers={"User-Agent": self.user_agent}).text
        iframe = re.findall(r"iframe src=\"(http:\/\/www\.sawlive\.tv\/.+?)\"", r)[0]
        return sawlive.Sawlive().get_link(iframe)