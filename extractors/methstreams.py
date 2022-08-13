import requests, re, base64
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta, datetime

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..scanners.m3u8_src import scan_page

class Methstreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["methstreams.com"]
        self.name = "Methstreams"
        self.short_name = "MS"
        
    def get_link(self, url):
        m3u8 = ""
        video_html = requests.get(url).text
        video = BeautifulSoup(video_html, "html.parser")
        if len(video.find_all("iframe")) > 0:
            iframe = video.find("iframe").get("src")
            r_iframe = requests.get(iframe).text
            atob = re.findall(r'window.atob\("(.+?)"\)', r_iframe)[0]
            m3u8 = Link(address=base64.b64decode(atob).decode("utf-8"), headers={"User-Agent": self.user_agent, "Referer": iframe})
        else:
            m3u8 = scan_page(url, video_html)
        return m3u8

    def get_games(self):
        games = []
        r = requests.get(f"http://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul.navbar-nav > li > a")
        for category in categories:
            league = category.text.replace(" streams", "")
            league_href = f"http://{self.domains[0]}{category.get('href')}"
            r_league = requests.get(league_href).text
            soup_league = BeautifulSoup(r_league, "html.parser")
            league_games = soup_league.find_all("a", {"class": "btn-block"})
            for body in league_games:
                href = body.get("href")
                title = body.find("h4").text.strip()
                time = body.find("p").text
                utc_time = None
                if time != "":
                    try:
                        utc_time = parse(time) + timedelta(hours=4)
                    except:
                        try:
                            utc_time = datetime.strptime(time, "%H:%M %p ET - %m/%d/%Y") + timedelta(hours=4)
                        except:
                            pass
                games.append(Game(title=title, links=[Link(address=href)], icon="-", league=league, starttime=utc_time))
        return games
