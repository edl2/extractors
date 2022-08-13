import requests, re
from ..models.Extractor import Extractor
from ..models.Link import Link
from ..util import jsunpack

class Sawlive(Extractor):
    def __init__(self) -> None:
        self.domains = ["sawlive.tv", "www.sawlive.tv"]

    def get_link(self, url):
        r = requests.get(url, headers={"User-Agent": self.user_agent}).text
        re_js = jsunpack.unpack(re.compile(r"(eval\(function\(p,a,c,k,e,d\).+?{}\)\))").findall(r)[0])
        jameiei = eval(re.findall(r"var jameiei=(\[.+?\])", re_js)[0])
        m3u8 = "".join([chr(x) for x in jameiei])
        return Link(address=m3u8)