import requests, re
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..scanners import m3u8_src

class AllSportsDaily(Extractor):
    def __init__(self) -> None:
        self.domains = ["allsportsdaily.co"]
        self.name = "AllSportsDaily"
        self.short_name = "ASD"

    def get_link(self, url):
        m3u8 = m3u8_src.scan_page(url)
        return m3u8
    
    def __get_games(self, url, league, page=1):
        games = []
        url = f"{url}/page/{page}"
        r = requests.get(url).text
        soup_league = BeautifulSoup(r, "html.parser")
        for game in soup_league.select("article"):
            header = game.find("a")
            game_href = header.get("href")
            game_title = header.text
            games.append(Game(title=game_title, links=[Link(game_href)], league=league))
        return games

    def get_games(self):
        games = []
        r = requests.get(f"http://{self.domains[0]}/live-event").text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("h1 > a")
        for category in categories:
            href = category.get("href")
            league = category.text.replace(" LIVE", "")
            games += self.__get_games(href, league)
            if league == "MLB":
                games += self.__get_games(href, league, 2)
        return games
