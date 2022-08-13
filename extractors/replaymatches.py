import requests
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class ReplayMatches(Extractor):
    def __init__(self) -> None:
        self.domains = ["replaymatches.net", "www.replaymatches.net"]
        self.name = "ReplayMatches"
        self.short_name = "RM"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}/search?q=*&max-results=50&by-date=true").text
        soup = BeautifulSoup(r, "html.parser")
        for game in soup.select("div.post-outer"):
            game_title = game.select_one("h2.post-title").text.strip()
            try: game_league = game.select_one("a.label-info").text
            except: game_league = ""
            game_href = game.select("a")[2].get("href")
            game_icon = game.select("img")[1].get("src")
            games.append(Game(title=game_title, icon=game_icon, league=game_league, links=[Link(address=game_href, is_links=True)]))
        return games

    def get_links(self, url):
        links = []
        r = requests.get(url).text
        soup = BeautifulSoup(r, "html.parser")
        if len(soup.select("a.link-iframe")) > 0:
            for link in soup.select("a.link-iframe"):
                embed = link.get("href")
                links.append(Link(address=embed, name=link.text))
        else:
            iframe = soup.select("iframe")[-1]
            links.append(Link(address=iframe.get("src"), name="Highlights"))
        return links
