import requests, re

from ..models.Extractor import Extractor
from ..models.Link import Link

class IPTVCat(Extractor):
    def __init__(self) -> None:
        self.domains = ["iptvcat.com", "list.iptvcat.com"]

    def get_link(self, url):
        if not url.endswith(".m3u8"): return url
        r = requests.get(url).text
        m3u8 = re.compile(r'(http(?:s?):\/\/.+?)\?').findall(r)[0]
        location = re.compile(r'http(?:s?):\/\/.+?\/').findall(m3u8)[0]
        endpoint = m3u8.replace(location, "")
        link = "%slive/%s.m3u8" % (location, endpoint)
        if "/live/live/" in link:
            link = link.replace("/live/live/", "/live/")
        if ".ts" in link:
            link = link.replace(".ts", "")
        return Link(address=link, jetproxy=True)