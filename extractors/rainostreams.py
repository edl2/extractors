import requests, re, datetime
from dateutil import parser
from ..scanners.m3u8_src import scan_page

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Rainostreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["rainostreams.com", "bdnewszh.com"]
        self.name = "Rainostreams"
        self.short_name = "RS"

    def get_link(self, url):
        if "rainostreams" in url:
            if "?sport" in url:
                url = url.split("?sport")[0]
            url = url.replace("https", "http").replace(self.domains[0], f"{self.domains[1]}/embed") + ".php"
        m3u8 = scan_page(url)
        if m3u8 != None:
            m3u8.headers["Referer"] = f"http://{self.domains[1]}/"
        return m3u8

    def get_games(self):
        games = []
        r = requests.get("http://streamsapi.xyz/mlb/live").json()
        r2 = requests.get("http://streamsapi.xyz/mlb/schedule").json()
        
        for game in r["results"] + r2["results"]:
            title = f"{game['home']['name']} vs {game['away']['name']}"
            if game["ss"] != None:
                title = "LIVE | " + title
            link = Link(f"http://{self.domains[1]}/embed/mlb/{game['home']['name'].split()[-1].lower()}.php")
            games.append(Game(
                title=title,
                links=[link],
                starttime=datetime.datetime.fromtimestamp(int(game['time'])) + datetime.timedelta(hours=7),
                league=game["league"]["name"]
            ))

        leagues = ["soccer", "nfl", "ncaaf", "nba", "nhl", "rugby", "race", "cricket", "mma"]
        for league in leagues:
            r = requests.get(f"http://api.{self.domains[1]}/{league}.json").json()
            games_arr = r["games"] if "games" in r else r["game"]
            for game in games_arr:
                if "h2h" in game:
                    title = game["h2h"]
                elif "name" in game:
                    title = game["name"]
                elif "title" in game:
                    title = game["title"]
                elif "home_team_name" in game:
                    title = f"{game['home_team_name']} vs {game['away_team_name']}"
                else:
                    title = f"{game['home']['name']} vs {game['away']['name']}"
                
                if "league" in game:
                    game_league = game["league"]
                elif "raceType" in game:
                    game_league = game["raceType"]
                elif "turnament" in game:
                    game_league = game["turnament"].capitalize()
                elif "tournaments" in game:
                    game_league = game["tournaments"]
                else:
                    game_league = league.upper()

                if "stream" in game:
                    link = Link(f"http://{self.domains[1]}/embed/{league if 'raceType' not in game else game['raceType'].lower()}/{game['stream']}.php")
                else:
                    link = Link(f"http://{self.domains[1]}/embed/{league}/{game['home_team_name'].split()[-1].lower()}.php")
                
                games.append(Game(
                    title=title,
                    league=game_league,
                    links=[link]
                ))

        
        return games