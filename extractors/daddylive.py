from typing import Dict
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..scanners import m3u8_src
import requests, re
from . import wstream, nbastreams
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from dateutil import parser
from datetime import datetime, timedelta
from ..icons import icons

class Daddylive(Extractor):
    def __init__(self) -> None:
        self.domains = ["daddylive.one", "daddylive\..+"]
        self.domains_regex = True
        self.name = "Daddylive"
        self.short_name = "DLive"

    # https://stackoverflow.com/questions/21496246/how-to-parse-date-days-that-contain-st-nd-rd-or-th
    def solve(self, s):                                             
        return re.sub(r'(\d)(st|nd|rd|th)', r'\1', s)

    def parse_header(self, header, time):
        timestamp = parser.parse(header[:header.index("-")] + " " + time)
        timestamp = timestamp.replace(year=2022) # daddylive is dumb
        return timestamp

    def get_link(self, url):
        m3u8 = ""
        if "/embed/" not in url and "/channels/" not in url and "/stream/" not in url and "/cast/" not in url and "/batman/" not in url:
            raise Exception("Invalid URL")
        # url = url.replace("/cast/", "/stream/").replace("/stream/", "/embed/").replace("/batman/", "/embed/")
        r = requests.get(url).text
        m3u8 = None
        if "wigistream.to" in r:
            re_embed = re.compile(r'src="(https:\/\/wigistream\.to\/embed\/.+?)"').findall(r)[0]
        elif "wstream.to" in r:
            re_embed = re.compile(r'src="(https:\/\/wstream\.to\/embed\/.+?)"').findall(r)[0]
        elif "eplayer.click" in r:
            re_embed = re.compile(r"<iframe src=\"(https:\/\/.+?)\"").findall(r)[0]
            r_embed = requests.get(re_embed, headers={"Referer": url}).text
            m3u8 = nbastreams.NBAStreams().process_page(r_embed, re_embed)
        elif "/embed/" in r:
            re_embed = re.compile(r'src="(https:\/\/.+?embed\/.+?)"').findall(r)[0]
        elif "castmax.net" in r:
            embed_id = re.compile(r"id='(.+?)'").findall(r)[0]
            re_embed = "https://castmax.net/embed/%s.html" % embed_id 
        elif "jazzy.to" in r:
            re_embed = re.findall(r'src="(https:\/\/jazzy\.to.+?)"', r)[0]
            m3u8 = m3u8_src.scan_page(re_embed, headers={"Referer": url})
        if m3u8 == None:
            try:
                m3u8 = wstream.Wstream().get_link(re_embed + f"|Referer=https://{self.domains[0]}")
            except:
                m3u8 = nbastreams.NBAStreams().process_page(r, url)
        return m3u8

    def get_games(self):
        games = []
        r_index = requests.get("https://" + self.domains[0] + "/index.php", headers={"User-Agent": self.user_agent}).text
        soup_index = BeautifulSoup(r_index, "html.parser")
        m: Dict[str, Game] = {}
        # league = ""
        header = soup_index.select_one("div.alert > center > h3 > strong").text
        # for element in list(soup_index.select("article.col-xs-12").children):
        #     try:
        #         if element == "\n":
        #             continue
        #         if element.name == "div" and (element.contents[1].name == "h3" or element.contents[1].name == "h4"):
        #             league = element.text
        #         elif element.name == "div" and element.contents[1].name == "h1":
        #             header = element.contents[1].contents[0].contents[0].text
        #         elif element.name == "p":
        #             league_games = str(element).replace("<br/>", "<br>").split("<br>")
        #             for game in league_games:
        #                 try:
        #                     game = "<p>" + game if not game.startswith("<p>") else game
        #                     game = game + "</p>" if not game.endswith("</p>") else game
        #                     soup_game = BeautifulSoup(game, "html.parser")
        #                     title = soup_game.contents[0].contents[1].strip()
        #                     time = title[0:title.index(" ")][:5]
        #                     try: utc_time = self.parse_header(header, time) - timedelta(hours=1)
        #                     except: utc_time = datetime.now().replace(hour=int(time.split(":")[0]), minute=int(time.split(":")[1])) - timedelta(hours=1)
        #                     if utc_time.hour < 10:
        #                         utc_time = utc_time + timedelta(days=1)
        #                     name = title[title.index(" ") + 1:]
        #                     hrefs = [Link(address=link) for link in map(lambda x: x.get("href"), soup_game.select("a"))]
        #                     games.append(Game(title=name, links=hrefs, icon=icons[league.strip().replace("\n", "").lower()], league=league.strip(), starttime=utc_time))
        #                 except Exception as e:
        #                     continue
        #     except:
        #         continue
        for element in soup_index.select('a[style="color: #ff0000;"]'):
            try:
                title = element.parent.find_previous_sibling("hr").next.strip()
                league = element.parent.find_previous("div", {"class": "alert"}).text.strip()
                time = title[0:title.index(" ")][:5]
                title = title[title.index(" ") + 1:]
                try: utc_time = self.parse_header(header, time) - timedelta(hours=1)
                except: 
                    try: utc_time = datetime.now().replace(hour=int(time.split(":")[0]), minute=int(time.split(":")[1])) - timedelta(hours=1)
                    except: utc_time = datetime.now()
                link = Link(address=element.get("href"), name=element.text)
                key = f"{league}:{title}@{time}"
                if key in m:
                    m[key].links.append(link)
                else:
                    m[key] = Game(title, links=[link], icon=icons[league.lower()] if league.lower() in icons else None, league=league, starttime=utc_time)
            except:
                continue

        games = list(m.values())
        return games