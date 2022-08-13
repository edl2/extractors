import requests, base64
from bs4 import BeautifulSoup
from ..models.Extractor import Extractor
from ..models.Link import Link
from ..models.Game import Game
from urllib.parse import urlparse, parse_qs

class Icelz(Extractor):
    def __init__(self) -> None:
        self.name = "Icelz"
        self.domains = ["icelz.newsrade.com"]

    def get_links(self, url):
        qs = parse_qs(urlparse(url).query)
        link = base64.b64decode(qs["id"][0]).decode("ascii")
        return [Link(address=link)]
    
    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}/tv/").text
        soup = BeautifulSoup(r, "html.parser")
        for option in soup.select("option"):
            value = option.get("value")
            if value == "":
                continue
            value = f"https://{self.domains[0]}{value}"
            name = option.text
            if "slingtv" in value:
                name += " (Sling)"
            games.append(Game(title=name, links=[Link(address=value, is_links=True)]))
        return games