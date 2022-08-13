import requests, time
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util.sportscentral_streams import get_streams_table

class SportsCentral(Extractor):
    def __init__(self) -> None:
        self.domains = ["sportscentral.io"]
        self.name = "SportsCentral"
        self.short_name = "SC"

    def get_games(self):
        games = []
        current_date = datetime.now()
        today = current_date.replace(hour=3, minute=0, second=0)
        date_format = current_date.strftime("%Y-%m-%d")

        leagues = ["nba", "nfl", "mlb", "nhl", "mma", "motorsport", "cricket",]
        for league in leagues:
            r = requests.get("https://sportscentral.io/api/%s-tournaments?date=%s" % (league, date_format), headers={"Referer": "https://redditmlbstreams.live", "User_Agent": self.user_agent}).json()
            for game_league in r:
                for event in game_league["events"]:
                    home_team = event["homeTeam"]["name"]
                    away_team = event["awayTeam"]["name"]
                    status = event["status"]["description"]
                    if status == None: status = "N/A"
                    if league != "mma":
                        home_score = event["homeScore"]["current"]
                        if home_score == "": home_score = "0"
                        away_score = event["awayScore"]["current"]
                        if away_score == "": away_score = "0"
                        title = "[COLORorange]%s %s-%s[/COLOR]: %s vs %s" % (status, home_score, away_score, home_team, away_team)
                    else:
                        title = "[COLORorange]%s[/COLOR]: %s vs %s" % (status, home_team, away_team)
                    icon = event["homeTeam"]["logo"]
                    game_id = event["id"]
                    game_time_str = "%sT%s" % (event["formatedStartDate"], event["startTime"])
                    game_time = datetime(*(time.strptime(game_time_str, "%Y-%m-%dT%H:%M")[:6]))
                    if game_time < today: continue
                    sport = event["sport"]
                    links_url = "https://sportscentral.io/streams-table/%s/%s?new-ui=1&origin=mlbstreams.to" % (str(game_id), sport)
                    games.append(Game(title=title, icon=icon, starttime=game_time, league=game_league["uniqueName"], links=[Link(links_url, is_links=True)]))
        
        # Soccer
        r = requests.get("https://sportscentral.io/new-api/matches?date=" + date_format, headers={"Referer": "https://redditmlbstreams.live", "User_Agent": self.user_agent}).json()
        for league in r:
            events = league["events"]
            logo = league["logo"]
            league_name = league["name"]
            for event in events:
                status = event["status"]["type"]
                if status != "inprogress": continue
                home_team = event["homeTeam"]["name"]
                home_score = event["homeScore"]["current"]
                away_team = event["awayTeam"]["name"]
                away_score = event["awayScore"]["current"]
                title = "[COLORorange]%s %s-%s[/COLOR]: %s vs %s" % (status.capitalize(), home_score, away_score, home_team, away_team)
                game_id = event["id"]
                game_time = datetime.fromtimestamp(event["startTimestamp"]) + timedelta(hours=7)
                links_url = "https://sportscentral.io/streams-table/%s/soccer?new-ui=1&origin=mlbstreams.to" % (str(game_id))
                games.append(Game(title=title, icon=logo, starttime=game_time, league=league_name, links=[Link(links_url, is_links=True)]))
        return games

    def get_links(self, url):
        return get_streams_table(url)
