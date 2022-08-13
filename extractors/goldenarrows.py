from ..models.Extractor import Extractor
from ..models.Link import Link
from ..models.Game import Game
import requests, re
from bs4 import BeautifulSoup
from . import wstream
from datetime import timedelta
from dateutil.parser import parse

class GoldenArrows(Extractor):
    def __init__(self) -> None:
        self.name = "GoldenArrows"
        self.domains = ["goldenarrowschannel.info"]
    
    def get_link(self, url):
        if "internal" not in url: url = url.replace("/stream", "/internal/stream")
        r = requests.get(url).text
        iframe = re.findall(r'iframe src="(.+?)"', r)[0]
        return wstream.Wstream().get_link(iframe + "|Referer=" + url)
    
    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}/internal/schedule-int.html").text
        soup = BeautifulSoup(r, "html.parser")
        for game in soup.select("tr"):
            game_date = game.contents[1].text.strip()
            if game_date == "Date": continue
            game_time = game.contents[3].text.strip()
            game_name = game.contents[7].text.strip()
            game_href = game.select("a")[-1].get("href")
            game_utc = parse(f"{game_date} {game_time}")
            games.append(Game(title=game_name, links=[Link(address=game_href)], starttime=game_utc, league="Darts"))
        return games