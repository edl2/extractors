from typing import List
import requests, re, json, time
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote
from ..models.Extractor import Extractor
from ..models.Link import Link
from ..models.Game import Game

class Weakspell(Extractor):
    def __init__(self) -> None:
        self.name = "Weakspell/LiveOnScore"
        self.short_name = "WS"
        self.domains = ["weakstreams.com", "sporteks.net", "liveonscore.tv", "wpstream.tv"]

    def get_link(self, url: str) -> Link:
        base_url = "http://" + urlparse(url).netloc
        r_game = requests.get(url).text
        re_vidgstream = re.compile(r'var vidgstream = "(.+?)";').findall(r_game)[0]
        if base_url == "http://liveonscore.tv":
            re_gethlsUrl = re.compile(r'gethlsUrl\(vidgstream, (.+?), (.+?)\);').findall(r_game)[0]
            r_hls = requests.get(base_url + "/gethls.php?idgstream=%s&serverid=%s&cid=%s" % (quote(re_vidgstream, safe=""), re_gethlsUrl[0], re_gethlsUrl[1]), headers={"User-Agent": self.user_agent, "Referer": url, "X-Requested-With": "XMLHttpRequest"}).text
        else:
            r_hls = requests.get(base_url + "/gethls.php?idgstream=%s" % quote(re_vidgstream, safe=""), headers={"User-Agent": self.user_agent, "Referer": url, "X-Requested-With": "XMLHttpRequest"}).text
        json_hls = json.loads(r_hls)
        m3u8 = json_hls["rawUrl"]
        if m3u8 == None:
            raise "no link found"
        else:
            m3u8 = Link(address=m3u8, headers={"Referer": url})
        return m3u8

    def get_games(self):
        games: List[Game] = []
        r = requests.get(f"http://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul.nav-menu > li > a")
        for category in categories:
            try:
                league = category.text.replace(" Streams", "")
                href = category.get("href")
                r_category = requests.get(href).text
                soup = BeautifulSoup(r_category, "html.parser")
                for game in soup.find_all("div", class_="competition"):
                    try:
                        re_url = re.compile(r'<a href="(.+?)">').findall(game.decode_contents())[0]
                        re_game = re.compile(r'<span class="competition-cell-table-cell competition-cell-side1"><span class="name"> (.+?) <\/span><span class="logo"><img.+?src="(.+?)".+?><\/span><\/span><span class="competition-cell-table-cell competition-cell-score"><i class="fa fa-clock"><\/i><span class="competition-cell-status">(.+?)<\/span><\/span><span class="competition-cell-table-cell competition-cell-side2"><span class="logo"><img.+?src="(.+?)".+?><\/span><span class="name"> (.+?)<\/span><\/span>').findall(game.decode_contents())[0]
                        title = "%s vs %s" % (re_game[0], re_game[4])
                        time_str = re_game[2].replace(" ,", ",")
                        utc_time = ""
                        if time_str != "":
                            if "LIVE" in time_str: utc_time = datetime.now(timezone.utc)
                            else: utc_time = datetime(*(time.strptime(time_str + " 2021", "%b %d, %I:%M %p %Y")[:6])) + timedelta(hours=5)
                        games.append(Game(title=title, links=Link(address=re_url), icon=re_game[1], league=league, starttime=utc_time))
                    except Exception as e:
                        continue
            except:
                continue
        return games