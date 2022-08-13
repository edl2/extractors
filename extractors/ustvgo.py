import requests, re
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class USTVGO(Extractor):
    def __init__(self) -> None:
        self.domains = ["ustvgo.tv"]
        self.name = "USTVGO"
        self.short_name = "USTVGO"

    def get_link(self, url):
        r = requests.get(url).text
        channel_id = re.compile(r"\?stream=(.+?)'").findall(r)[0]
        # m3u8 = requests.post("https://ustvgo.tv/data.php", data={"stream": channel_id}).text
        iframe = requests.get("https://ustvgo.tv/player.php?stream=" + channel_id, headers={"Referer": url}).text
        m3u8 = re.findall(r"var hls_src='(.+?)'", iframe)[0]
        return Link(m3u8)

    def get_games(self):
        games = []
        r = requests.get("https://ustvgo.tv/").text
        soup = BeautifulSoup(r, "html.parser")
        channels = soup.select("ol > li")
        for channel in channels:
            link = channel.select_one("a")
            games.append(Game(title=link.text, links=[Link(link.get("href"))]))
        return games