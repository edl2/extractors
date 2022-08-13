from ..models.Extractor import Extractor
from ..models.Link import Link
import requests, re
from . import wstream, daddylive

class CaspTV(Extractor):
    def __init__(self) -> None:
        self.domains = [".+casptv.xyz"]
        self.domains_regex = True

    def get_link(self, url: str) -> Link:
        r_casptv = requests.get(url).text
        embed = re.findall(r'<iframe src="(.+?)"', r_casptv)[0]
        if "daddylive" in embed:
            return daddylive.Daddylive().get_link(embed)
        rowsports = re.findall(r'iframe.+?src="(.+?)"', r_casptv)[0]
        r_rowsports = requests.get(rowsports).text
        if "fid" in r_rowsports:
            fid = re.findall(r'fid="(.+?)"', r_rowsports)[0]
            r_pkcast = requests.get(f"https://www.pkcast123.me/footy.php?player=desktop&live={fid}&vw=740&vh=416", headers={"Referer": "https://1rowsports.com"}).text
            m3u8 = "".join(eval(re.findall(r"return\((\[.+?\])", r_pkcast)[0])).replace("\\", "")
            return Link(address=m3u8, headers={"Referer": "https://www.pkcast123.me/"})
        elif "wigistream" in r_rowsports:
            wigi = re.findall(r'<iframe src="(.+?)"', r_rowsports)[0]
            return wstream.Wstream().get_link(wigi + "|Referer=" + rowsports)
    
