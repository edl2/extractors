from ..scanners import m3u8_src
from ..models.Extractor import Extractor
from ..models.Link import Link
from . import embedstream, daddylive, cloudstream, okru
import requests, re, base64
from bs4 import BeautifulSoup

class NBAStreams(Extractor):
    def __init__(self) -> None:
        self.name = "NBAStreams"
        self.domains = ["nba-streams.online"]
    
    def get_links(self, url):
        r = requests.get(url).text
        soup = BeautifulSoup(r, "html.parser")
        links = [Link(address=link.get("href"), name=link.text) for link in soup.select("a")]
        return links
    
    def __check_valid_link(self, link):
        valid = ["primetubsub", "ok.ru", "embedstream", "funks.ws", "daddylive", "nba-streams", "wizhdlive", "player.licenses4.me"]
        for v in valid:
            if v in link:
                return True
        return False
    
    def process_page(self, r, referer):
        iframe = list(filter(lambda x: self.__check_valid_link(x), re.findall(r'<iframe.+?src="(.+?)"', r)))[0]
        if iframe.startswith("//"):
            iframe = "https:" + iframe
        if "poscitech" in iframe:
            player_id = re.findall(r'player\/ch(.+?)\.php', r)[0]
            widevine = f"https://widevine.licenses4.me/mdl.p2p.php?id=premium{player_id}&test=true"
            r_widevine = requests.get(widevine, headers={"Referer": "https://eplayer.click"}).text
            source = re.findall(r"source:'(.+?)',", r_widevine)[-1]
            return Link(address=source, headers={"Referer": widevine})
        elif "player.licenses4.me" in iframe:
            r_widevine = requests.get(iframe, headers={"Referer": "https://rkc.primetubsub.xyz/"}).text
            source = re.findall(r"source:'(.+?)',", r_widevine)[-1]
            return Link(address=source, headers={"Referer": iframe})
        elif "primetubsub" in iframe:
            player_id = re.findall(r"id=(.+)", iframe)[0]
            # widevine = f"https://widevine.licenses4.me/mdl.p2p.php?id=premium{player_id}&test=true"
            widevine = f"https://player.licenses4.me/player.php?id=premium{player_id}&test=true"
            r_widevine = requests.get(widevine, headers={"Referer": "https://rkc.primetubsub.xyz/"}).text
            source = re.findall(r"source:'(.+?)',", r_widevine)[-1]
            return Link(address=source, headers={"Referer": widevine})
        elif "ok.ru" in iframe:
            return okru.OkRu().get_link(iframe)
        elif "embedstream" in iframe:
            return embedstream.Embedstream().get_link(iframe)
        elif "funks.ws" in iframe:
            return m3u8_src.scan_page(iframe, headers={"Referer": referer, "User-Agent": self.user_agent})
        # elif "daddylive" in iframe:
        #     return daddylive.Daddylive().get_link(iframe)
        elif "nba-streams" in iframe:
            r = requests.get(iframe).text
            if "var strm" in r:
                strm = re.findall(r"var strm = window\.atob\('(.+?)'\)", r)[0]
                return Link(address=base64.b64decode(strm).decode("ascii"))
            else:
                return m3u8_src.scan_page(iframe)
        elif "wizhdlive" in iframe:
            r = requests.get(iframe).text
            iframe = re.findall(r'<iframe.+?src="(.+?)"', r)[0]
            return cloudstream.CloudStream().get_link(iframe)
        else:
            scan = m3u8_src.scan_page(iframe, headers={"Referer": referer})
            if scan is not None:
                if "?auth=" in scan.address:
                    scan.address = scan.address.split("?")[0]
                return scan
            else:
                return Link(address=iframe)

    def get_link(self, url):
        r = requests.get(url).text
        return self.process_page(r)
