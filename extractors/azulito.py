import requests, re
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Azulito(Extractor):
    def __init__(self) -> None:
        self.domains = ["fabtech.work"]
        self.name = "Azulito"
        self.short_name = "AZ"

    def get_link(self, url):
        r = requests.get(url).text
        m3u8 = re.findall(r"source src=\"(.+?)\"", r)[0]
        return Link(address=m3u8, headers={"Referer": url})

    def get_games(self):
        games = []
        r = requests.get("https://" + self.domains[0]).text
        soup = BeautifulSoup(r, "html.parser")
        for game in soup.select("li.g1-collection-item"):
            title = game.select_one("h3.entry-title").text
            href = game.select_one("a").get("href")
            icon = game.select_one("img").get("src")
            try: league = game.select_one("a.entry-category").text.replace(" Streams", "")
            except: league = None
            games.append(Game(title=title, links=[Link(address=href)], icon=icon, league=league))
        return games
