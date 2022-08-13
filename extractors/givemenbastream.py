import requests, re

from ..models.Extractor import Extractor
from ..models.Link import Link
from ..scanners import clappr

class GiveMeNBAStreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["givemenbastreams.com", "givemenflstreams.com"]

    def get_link(self, url):
        r = requests.get(url).text
        iframe = re.findall(r'iframe class=\"embed-responsive-item\" src=\"(.+?)\"', r)[0]
        return Link(address=clappr.scan_page(iframe))