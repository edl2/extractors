import requests, time,base64
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class V2Sportsurge(Extractor):
    def __init__(self) -> None:
        self.domains = ["v2.sportsurge.net"]
        self.name = "V2 Sportsurge"

    def get_links(self, url):
        links = []
        r = requests.get(url).text
        soup = BeautifulSoup(r, "html.parser")
        exclude = requests.get(base64.b64decode("aHR0cHM6Ly9tYWduZXRpYzEucmF0cGFjay5hcHBib3hlcy5jby9NQURfVElUQU5fU1BPUlRTL1NQT1JUUy9TSVRFUy9zaXRlX2V4Y2x1ZGUuanNvbg==").decode("utf-8")).json()
        for stream in soup.select(".game-forecast-link.MobildeGizle"):
            name = stream.select_one("h4").text
            if name in exclude:
                continue
            href = stream.select_one("td").get("data-href")
            links.append(Link(address=href, name=name))
        return links

    def get_games(self):
        games = []
        r = requests.get("https://" + self.domains[0]).text
        soup = BeautifulSoup(r, "html.parser")
        for game in soup.select(".MaclariListele"):
            teams = game.select("h4")
            try: title = teams[0].text.strip() + " vs. " + teams[1].text.strip()
            except: title = teams[0].text.strip()
            category = game.select_one(".col-1").text.strip()
            date = game.select_one(".col-4").text.strip()
            utc_time = datetime(*(time.strptime(date, "%m/%d/%Y %I:%M %p ET")[:6])) + timedelta(hours=4)
            try: icon = f'https://{self.domains[0]}/{game.select_one("img").get("src")}'
            except: icon = ""
            href = f'https://{self.domains[0]}/{game.get("href")}'
            games.append(Game(title=title, icon=icon, starttime=utc_time, league=category, links=[Link(href, is_links=True)]))
        return games