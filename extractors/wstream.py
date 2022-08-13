import requests, re

from ..models.Extractor import Extractor
from ..models.Link import Link
from ..util import jsunpack
from ..scanners import m3u8_src
from urllib.parse import parse_qs

class Wstream(Extractor):
    def __init__(self) -> None:
        self.domains = ["wstream.to", "wigistream.to"]

    def get_link(self, url: str) -> Link:
        options = url.split("|")
        if len(options) < 2 or "referer" not in options[1].lower():
            raise Exception("Must have referer in URL")
        url = url.replace("|" + options[1], "")
        parsed_qs = parse_qs(options[1].lower())
        r = requests.get(url, headers={"Referer": parsed_qs["referer"][0]}).text
        if len(re.findall(r'source\s+?:\s+?"(.+?)"', r)) > 0:
            m3u8 = re.compile(r'source\s+?:\s+?"(.+?)"').findall(r)[0]
        elif len(re.findall(r'src\s+?:\s+?"(.+?)"', r)) > 0:
            m3u8 = re.findall(r'src\s+?:\s+?"(.+?)"', r)[0]
        else:
            re_js = jsunpack.unpack(re.compile(r"(eval\(function\(p,a,c,k,e,d\).+?{}\)\))").findall(r)[0])
            m3u8 = m3u8_src.scan_page(url, re_js)
        m3u8.is_ffmpegdirect = True
        return m3u8