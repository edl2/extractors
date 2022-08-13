import requests, re, time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from ..models.Extractor import Extractor
from urllib.parse import urlparse

from ..models.Game import Game
from ..models.Link import Link
from ..util import sportscentral_streams

class NBABite(Extractor):
    def __init__(self) -> None:
        self.domains = ["scor.nbabite.com", "reddit.nflbite.com", "nhlbite.com", "mlbshow.com", "cricketstreams.cc", "main.formula1stream.cc", "original.mmastreams.cc", "original.boxingstreams.cc", "wwestreams.cc", "olympicstreams.net"]
        self.name = "NBAbite"
        self.short_name = "NBAB"

    def get_games(self):
        games = []
        for site in self.domains:
            try:
                r = requests.get("https://" + site).text
                soup = BeautifulSoup(r, "html.parser")
                date = datetime(*(time.strptime(soup.select_one("div.date").text.strip(), "%a %d %b %Y")[:6]))
                other_sites = soup.select("a.other-site")
                league = ""
                for other_site in other_sites:
                    if urlparse(other_site.get("href")).netloc == site:
                        league = other_site.select_one("div.site-name").text.strip().replace(" Streams", "")
                if "olympic" in site:
                    for competition in soup.select("div.competition"):
                        competition_name = competition.select_one("div.name").text
                        for game in soup.select("div.col-md-12"):
                            title = game.select_one("div.team-name").text
                            href = game.select_one("a").get("href")
                            games.append(Game(title=title, league=f"{league} {competition_name}", links=[Link(address=href, is_links=True)]))
                else:
                    for game in soup.select("div.col-md-6"):
                        team_names = [team.text for team in game.select("div.team-name")]
                        title = "%s vs %s" % (team_names[0], team_names[1])
                        status = game.select_one("div.status")
                        game_time = None
                        if "live-indicator" not in status.attrs["class"] and ":" in status.text:
                            split = status.text.split(":")
                            hour = int(split[0])
                            minute = int(split[1])
                            game_time = date.replace(hour=hour, minute=minute) + timedelta(hours=4)
                        else:
                            title = "[COLORyellow]%s[/COLOR] - %s" % (status.text, title)
                        score = game.select("div.score")
                        if len(score) > 0 and score[0].text:
                            scores = [i.text for i in score]
                            title =  "%s [COLORyellow](%s-%s)[/COLOR]" % (title, scores[0], scores[1])
                        icon = game.select_one("img").get("src")
                        href = game.select_one("a").get("href")
                        games.append(Game(title=title, icon=icon, starttime=game_time, league=league, links=[Link(address=href, is_links=True)]))
            except:
                continue
        
        return games

    def get_links(self, url):
        r = requests.get(url).text
        match_id = re.findall(r"var streamsMatchId = (.+?);", r)[0]
        match_sport = re.findall(r"var streamsSport = \"(.+?)\"", r)[0]
        streams = sportscentral_streams.get_streams(match_id, match_sport, self.domains[0])
        return streams


