from ..models.Extractor import Extractor
from ..models.Link import Link
import requests, re
from ..util import jsunpack

class CloudStream(Extractor):
    def __init__(self) -> None:
        self.domains = ["cloudstream.to"]
    
    def get_link(self, url):
        r = requests.get(url, headers={"Referer": url}).text
        re_js = jsunpack.unpack(re.compile(r"(eval\(function\(p,a,c,k,e,d\).+?{}\)\))").findall(r)[0])
        m3u8 = re.findall(r'var src.?=.?"(.+?)"', re_js)[0]
        return Link(address=m3u8, headers={"Referer": url})