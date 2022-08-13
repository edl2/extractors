import requests
import multiprocessing as mp
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Sofascore(Extractor):
    def __init__(self) -> None:
        self.disabled = True
        self.domains = ["redditsport.live"]

    def __get_games(self, sport):
        games = []
        r = requests.get(f"https://api.sofascore.com/api/v1/sport/{sport}/events/live").json()
        for event in r["events"]:
            game_title = f"{event['homeTeam']['name']} vs {event['awayTeam']['name']}"
            games.append(Game(title=game_title, icon=f"https://www.sofascore.com/static/images/flags/{event['tournament']['category']['alpha2'].lower()}.png", league=event["tournament"]["name"], starttime=datetime.fromtimestamp(event["startTimestamp"]), links=Link(address=f"https://{self.domains[0]}/streams.json?id={event['id']}")))
        return games

    def get_games(self):
        games = []
        http_proxy  = "http://3.211.65.185:80"
        https_proxy  = "http://3.211.65.185:80"
        ftp_proxy   = "10.10.1.10:3128"

        proxyDict = {
                    "http"  : http_proxy,
                    "https" : https_proxy,
                    "ftp"   : ftp_proxy
                    }
        event_count = requests.get("https://api.sofascore.com/api/v1/sport/-28800/event-count", proxies=proxyDict)
        # for event, count in event_count.items():
        #     if count["live"] > 0:
                
        return games
        
    def get_links(self, url):
        r = requests.get(url).json()
        game_id = parse_qs(urlparse(url).query)["id"]
        streams = filter(lambda x: x["event"] == game_id, r)
        links = [Link(address=stream["link"]) for stream in streams]
        return links